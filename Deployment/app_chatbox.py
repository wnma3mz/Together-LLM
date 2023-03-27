import gradio as gr
import requests

max_q = 3 # Only three historical conversations are kept
chatapi_url = ""


def simple_template(prompt):
    return f"""
### Instruction:
{prompt}

### Response:
"""


his_token_ids_lst = None


def reply_text(prompt):
    #
    prompt = simple_template(prompt)
    post_json = {"prompt": prompt}
    if his_token_ids_lst:
        post_json["embd_inp_arr"] = [his_token_ids_lst[0]] + [
            x for x in his_token_ids_lst[1:][-max_q:]
        ]
    s = requests.post(chatapi_url, json=post_json)
    results = s.json()["results"][0]
    # str, List[List[int]]
    return results["text"], results["token_ids_lst"]


def add_text(history, text):
    # Question, Answer, TokenIds
    history = history + [[text, None]]
    return history, ""


def add_file(history, file):
    # Temporarily out of use
    history = history + [((file.name,), None)]
    return history


def bot(history):
    response, token_ids_lst = reply_text(history[-1][0])
    # Default Template TokenIds Or Called Background
    global his_token_ids_lst
    if his_token_ids_lst is None:
        his_token_ids_lst = [token_ids_lst[0]]
    history[-1][1] = response
    his_token_ids_lst.append(token_ids_lst[-1])
    return history


def clean_func():
    global his_token_ids_lst
    his_token_ids_lst = None


with gr.Blocks(
    css="#loc {margin: auto} .feedback {font-size: 24px} #bc {background-color: lightgrey}"
) as demo:
    chatbot = gr.Chatbot([], elem_id="chatbot").style(height=500)
    with gr.Row():
        with gr.Column(scale=0.85):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter, or upload an image",
            ).style(container=False)
        with gr.Column(scale=0.15, min_width=0):
            btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])

    clear = gr.Button("Clear")

    txt.submit(add_text, [chatbot, txt], [chatbot, txt]).then(bot, chatbot, chatbot)
    btn.upload(add_file, [chatbot, btn], [chatbot]).then(bot, chatbot, chatbot)
    clear.click(clean_func, None, chatbot, queue=False)

if __name__ == "__main__":
    # network_test()
    gr.close_all()
    # demo.queue(concurrency_count=3, max_size=20)
    demo.launch(
        debug=True,
        server_name="0.0.0.0",
        server_port=7860,
        # ssl_keyfile="./localhost+2-key.pem",
        # ssl_certfile="./localhost+2.pem",
    )
