import openai, asyncio, time
import PySimpleGUI as sg
from decouple import config

openai.api_key = config('GPT')
sg.theme('Topanga')

async def resp(*, pergunta: str):
    resp = openai.Completion.create(
        engine="text-davinci-003",
        prompt=pergunta,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
        presence_penalty=0.6,
        frequency_penalty=0.5,
        #context="Estou conversando com um usuário no discord em pt-bt"
    )
    msg = resp.choices[0].text.strip()
    return msg

async def animate_text(output_element, text):
    for char in text:
        print(char, end='', flush=True)
        await asyncio.sleep(0.05)
    print()
    output_element.update(value=text)  # Atualiza o elemento sg.Output

async def main():
    layout = [
        [sg.Text('Pergunta:')],
        [sg.Multiline(key='perg', size=(50, 1))],
        [sg.Button('enviar')],
        [sg.Text('Resposta:')],
        [sg.Output(key='rs', size=(50, 10))]
    ]

    janela = sg.Window('GPTzada', layout, icon='img/icone.ico')
    while True:
        eventos, valores = janela.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        elif eventos == 'enviar':
            try:
                pergunta = valores['perg']
                resposta = await resp(pergunta=pergunta)
                await animate_text(janela['rs'], resposta)
            except ValueError:
                sg.popup('Digite uma pergunta.')

    janela.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())