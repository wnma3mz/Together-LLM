import ctypes
import os
import time
from flask import Flask, Response, jsonify, make_response, render_template, request

app = Flask(__name__)


class load_model_inputs(ctypes.Structure):
    _fields_ = [
        ("threads", ctypes.c_int),
        ("max_context_length", ctypes.c_int),
        ("batch_size", ctypes.c_int),
        ("model_filename", ctypes.c_char_p),
        ("n_parts_overwrite", ctypes.c_int),
    ]


class generation_inputs(ctypes.Structure):
    _fields_ = [
        ("seed", ctypes.c_int),
        ("prompt", ctypes.c_char_p),
        ("max_context_length", ctypes.c_int),
        ("max_length", ctypes.c_int),
        ("temperature", ctypes.c_float),
        ("top_k", ctypes.c_int),
        ("top_p", ctypes.c_float),
        ("rep_pen", ctypes.c_float),
        ("rep_pen_range", ctypes.c_int),
    ]


class generation_outputs(ctypes.Structure):
    _fields_ = [
        ("status", ctypes.c_int),
        ("text", ctypes.c_char * 16384),
        ("token_id", ctypes.c_int * 16384),
    ]


dir_path = os.path.dirname(os.path.realpath(__file__))
handle = ctypes.CDLL(dir_path + "/llamacpp-for-kobold/llamacpp.dll")

handle.load_model.argtypes = [load_model_inputs]
handle.load_model.restype = ctypes.c_bool
handle.generate.argtypes = [
    generation_inputs,
    ctypes.c_wchar_p,
    ctypes.POINTER(ctypes.c_int),
    ctypes.c_int,
]  # apparently needed for osx to work. i duno why they need to interpret it that way but whatever
handle.generate.restype = generation_outputs


handle.prompt_tokenize_py.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]


def array2lst(array):
    lst = []
    for x in array:
        if x == -1 or x == 0:
            break
        lst.append(x)
    return lst


def prompt_tokenize(prompt):
    n = 16384
    result_array = (ctypes.c_int * n)(*[-1 for _ in range(n)])

    handle.prompt_tokenize_py(prompt.encode("UTF-8"), result_array)
    return array2lst(result_array)


def load_model(
    model_filename, batch_size=8, max_context_length=512, n_parts_overwrite=-1
):
    inputs = load_model_inputs()
    inputs.model_filename = model_filename.encode("UTF-8")
    inputs.batch_size = batch_size
    inputs.max_context_length = (
        max_context_length  # initial value to use for ctx, can be overwritten
    )
    inputs.threads = 12
    # inputs.threads = os.cpu_count()
    inputs.n_parts_overwrite = n_parts_overwrite
    ret = handle.load_model(inputs)
    return ret


def generate(
    prompt,
    max_length=20,
    max_context_length=512,
    temperature=0.8,
    top_k=100,
    top_p=0.85,
    rep_pen=1.1,
    rep_pen_range=128,
    seed=-1,
    embd_inp_arr=None,
):
    inputs = generation_inputs()
    outputs = ctypes.create_unicode_buffer(ctypes.sizeof(generation_outputs))
    inputs.prompt = prompt.encode("UTF-8")
    inputs.max_context_length = (
        max_context_length  # this will resize the context buffer if changed
    )
    inputs.max_length = max_length
    inputs.temperature = temperature
    inputs.top_k = top_k
    inputs.top_p = top_p
    inputs.rep_pen = rep_pen
    inputs.rep_pen_range = rep_pen_range
    inputs.seed = seed

    if embd_inp_arr:
        embd_inp_arr_n = len(embd_inp_arr)
    else:
        embd_inp_arr_n = 1
        embd_inp_arr = []

    ret = handle.generate(
        inputs,
        outputs,
        (ctypes.c_int * embd_inp_arr_n)(*embd_inp_arr),
        ctypes.c_int(embd_inp_arr_n),
    )
    if ret.status == 1:
        return ret.text.decode("UTF-8"), array2lst(ret.token_id)
    return "", []


maxctx = 2048
# maxctx = 512
maxlen = 128
mdl_nparts = 1
modelname = "llamacpp-for-kobold/models/7B/ggml-model-quant.bin"
# modelname = "llamacpp-for-kobold/models/65B/ggml-model-q4_0.bin"
loadok = load_model(modelname, 8, maxctx, mdl_nparts)


genparams = {
    "max_length": 50,
    "temperature": 0.2,
    "top_k": 100,
    "top_p": 1,
    "rep_pen": 1.1,
    "rep_pen_range": 128,
}


def func(prompt, genparams=genparams, embd_inp_arr=None):
    s1 = time.time()
    recvtxt, token_ids = generate(
        prompt=prompt,
        max_length=genparams.get("max_length", 50),
        temperature=genparams.get("temperature", 0.8),
        top_k=genparams.get("top_k", 100),
        top_p=genparams.get("top_p", 0.85),
        rep_pen=genparams.get("rep_pen", 1.1),
        rep_pen_range=genparams.get("rep_pen_range", 128),
        seed=0,
        embd_inp_arr=embd_inp_arr,
    )
    print("Cost Time:", time.time() - s1)
    return recvtxt, token_ids


def preprocess(text, **kwargs):
    return text


def postprocess(text, **kwargs):
    text_lst = text.split("\n")
    for output in text_lst:
        if output:
            break
        else:
            output = ""
    return output


init_template = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n"


@app.route("/api/chat", methods=["POST"])
def chat_f():
    if request.method == "POST":
        post_genparams = request.json

        prompt = post_genparams.get("prompt", "")

        for key in genparams.keys():
            if key in post_genparams:
                genparams[key] = post_genparams[key]

        if post_genparams.get("embd_inp_arr", None):
            embd_inp_arr = post_genparams.get("embd_inp_arr")  # List[List[int]]
        else:
            embd_inp_arr = [prompt_tokenize(init_template)]

        prompt = preprocess(prompt, **post_genparams)
        output, token_ids = func(
            prompt, genparams, [x for x_lst in embd_inp_arr for x in x_lst]
        )
        output = postprocess(output, **post_genparams)

        embd_inp_arr += [token_ids]
        return jsonify({"results": [{"text": output, "token_ids_lst": embd_inp_arr}]})
    else:
        return jsonify({"status": 204})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6002, debug=False)
