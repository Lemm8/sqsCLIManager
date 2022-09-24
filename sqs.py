import boto3
import botocore
from dotenv import load_dotenv
import os
import re
load_dotenv()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def create_queue( client ):
    while (True):
        name = input('Nombre del Queue: ')
        if not re.match('^[a-zA-Z0-9_-]+$', name):
            print( 'El nombre solo puede tener caractéres alfanuméricos, - y _. Vuelva a intentar' )

        # TODO: attributes
        # if not attributes:
        #     attributes = {}

        else:
            try:
                queue = client.create_queue( QueueName=name, Attributes={} )
                print( f'{queue} \n Se creó el queue "{name}". Url del queue: {bcolors.UNDERLINE}{bcolors.OKCYAN}{queue["QueueUrl"]}{bcolors.ENDC}' )
            except botocore.exceptions.ClientError as error:
                print(f'{bcolors.FAIL}Error:{bcolors.ENDC} {error} \n Ocurrió un error, no se puede crear el queue con el nombre "{bcolors.UNDERLINE}{name}{bcolors.ENDC}"')
            break
    print('\n')


def list_queue( client ):
    while (True):
        try:
            queues = client.list_queues()["QueueUrls"]
            i = 1
            print( f'{bcolors.OKBLUE}QUEUES{bcolors.ENDC}' )
            for queue in queues:
                print( f'{i} - {bcolors.UNDERLINE}{bcolors.OKCYAN}{queue}{bcolors.ENDC}' )
                i += 1
        except botocore.exceptions.ClientError as error:
            print(f'{bcolors.FAIL}Error: {bcolors.ENDC} {error} \n Ocurrió un error, no se pueden listar los SQS')
        break
    print('\n')

def delete_queue( client ):    
    while (True):
        queueUrl = input('Url del queue: ')
        try:
            response = client.delete_queue( QueueUrl= queueUrl )
            print( f' {response} \n {bcolors.OKBLUE} Se borró el queue con éxito {bcolors.ENDC} ' )
        except botocore.exceptions.ClientError as error:
            print(f'{bcolors.FAIL}Error: {bcolors.ENDC} {error} \n Ocurrió un error, no se puede borrar el queue con la Url: {bcolors.UNDERLINE}{bcolors.OKCYAN}{queueUrl}{bcolors.ENDC}')        
        break
    print('\n')

def send_message( client ):
    while (True):
        queueUrl = input('Url del queue: ')
        messageBody = input('Cuerpo del mensaje: ')
        try:
            delaySeconds = int(input( 'Segundos de retraso: ' ))
            if delaySeconds >= 0 and delaySeconds <= 900:
                try:
                    response = client.send_message( QueueUrl=queueUrl, MessageBody=messageBody, DelaySeconds=delaySeconds )
                    print(f'{response} \n Se ha enviado el mensaje al queue: {bcolors.UNDERLINE}{bcolors.OKCYAN}{queueUrl}{bcolors.ENDC}')
                except botocore.exceptions.ClientError as error:
                    print(f'{bcolors.FAIL}Error: {bcolors.ENDC} {error} \n Ocurrió un error, no se puede enviar el mensaje al queue con la Url: {bcolors.UNDERLINE}{bcolors.OKCYAN}{queueUrl}{bcolors.ENDC}')
                break
            else:
                print('El valor tiene que estar entre 0 o 900')
        except ValueError:
                print('No es una opción válida, vuelva a intentar')
    print('\n')

def receive_message( client ):
    while(True):
        queueUrl = input('Url del queue: ')
        try:
            maxNumberOfMessages = int( input('Máximo número de mensajes (1min-10max): ') )
            waitTimeSeconds = int( input('Segundos de espera: ') )
            if maxNumberOfMessages >= 1 and maxNumberOfMessages <= 10:
                try:
                    response = client.receive_message( QueueUrl=queueUrl, MaxNumberOfMessages=maxNumberOfMessages, WaitTimeSeconds=waitTimeSeconds )
                    print(f'Se recibieron {bcolors.BOLD}{len(response.get("Messages", []))}{bcolors.ENDC} mensajes.')
                    for message in response['Messages']:
                        print(f'{bcolors.OKBLUE}Message Body{bcolors.ENDC}: {message["Body"]}')
                        print(f'{bcolors.WARNING}Recepit Handle{bcolors.ENDC}: {message["ReceiptHandle"]} \n')
                except botocore.exceptions.ClientError as error:
                    print(f'{bcolors.FAIL}Error: {bcolors.ENDC} {error} \n Ocurrió un error, no se pueden recibir los mensajes en el queue con la Url: {bcolors.UNDERLINE}{bcolors.OKCYAN}{queueUrl}{bcolors.ENDC}')
                break
            else:
                print('El numero de mensajes debe ser entre 1 y 10')
        except ValueError:
            print('No es una opción válida, vuelva a intentar')
    print('\n')

def delete_message( client ):
    while (True):
        queueUrl = input('Url del queue: ')
        receiptHandle = input('Último Receipt Handle: ')
        try:
            response = client.delete_message( QueueUrl=queueUrl, ReceiptHandle=receiptHandle )
            print(f'{response} \n Se ha eliminado el mensaje del queue: {bcolors.UNDERLINE}{bcolors.OKCYAN}{queueUrl}{bcolors.ENDC}')
        except botocore.exceptions.ClientError as error:
            print(f'{bcolors.FAIL}Error: {bcolors.ENDC} {error} \n Ocurrió un error, no se puede borrar el mensaje en el queue con la Url: {bcolors.UNDERLINE}{bcolors.OKCYAN}{queueUrl}{bcolors.ENDC}')
        break
    print('\n')

def tag_queue( client ):
    while(True):
        queueUrl = input('Url del queue: ')
        no_tags = int(input('Numero de tags: '))
        tags = {}
        for _ in range(no_tags):
            tag_name = input('Nombre del tag: ')
            tag_value = input('Valor del tag: ')
            tags[tag_name] = tag_value
        try:
            response = client.tag_queue( QueueUrl=queueUrl, Tags=tags )
            print(f'{response} \n Se añadieron los tags: ')
            for tag in tags:
                print( f'{bcolors.BOLD} {tag}: {bcolors.OKBLUE} {tags[tag]} {bcolors.ENDC}' )
            print(f'al queue con la url: {bcolors.UNDERLINE}{bcolors.OKCYAN}{queueUrl}{bcolors.ENDC}')
        except botocore.exceptions.ClientError as error:
            print(f'{bcolors.FAIL}Error: {bcolors.ENDC} {error} \n Ocurrió un error, no se pueden agregar los tags al queue con la Url: {bcolors.UNDERLINE}{bcolors.OKCYAN}{queueUrl}{bcolors.ENDC}')
        break
    print('\n')

def list_queue_tags( client ):
    while( True ):
        queueUrl = input('Url del queue: ')        
        try:
            response = client.list_queue_tags( QueueUrl=queueUrl )
            if len(response.get("Tags", [])) == 0:
                print(f'No hay tags en este queue')
            else:
                print(f'{bcolors.OKBLUE}Tags: {bcolors.ENDC} ')
                for tag in response['Tags']:
                    print(f'- {bcolors.BOLD} {tag}: {bcolors.OKGREEN}{response["Tags"][tag]}{bcolors.ENDC}')
        except botocore.exceptions.ClientError as error:
            print(f'{bcolors.FAIL}Error: {bcolors.ENDC} {error} \n Ocurrió un error, no se pueden listar los tags del queue con la Url: {bcolors.UNDERLINE}{bcolors.OKCYAN}{queueUrl}{bcolors.ENDC}')
        break
    print('\n')

def untag_queue( client ):
    while(True):
        queueUrl = input('Url del queue: ')
        tag_keys = []
        c = True
        print( 'Ingresa los tags a eliminar (ingresa 0 para salir)' )
        while(c == True):
            key = input('Tag: ')
            if key == '0':
                c = False
            else:
                tag_keys.append( key )
        try:
            response = client.untag_queue( QueueUrl=queueUrl, TagKeys=tag_keys )
            print(f'{response} \n se han borrado los tags {bcolors.OKBLUE} {tag_keys} {bcolors.ENDC} del queue con la Url: {bcolors.UNDERLINE}{bcolors.OKCYAN}{queueUrl}{bcolors.ENDC}')
        except botocore.exceptions.ClientError as error:
            print(f'{bcolors.FAIL}Error: {bcolors.ENDC} {error} \n Ocurrió un error, no se pueden borrar los tags del queue con la Url: {bcolors.UNDERLINE}{bcolors.OKCYAN}{queueUrl}{bcolors.ENDC}')
        break
    print('\n')

menu_options = {
    1: {
        "title": "List Queues",
        "action": list_queue
    },
    2: {
        "title": "Create Queue",
        "action": create_queue
    },
    3: {
        "title": "Delete Queue",
        "action": delete_queue
    },
    4: {
        "title": "Send Message",
        "action": send_message
    },
    5: {
        "title": "Receive Message",
        "action": receive_message
    },
    6: {
        "title": "Delete Message",
        "action": delete_message
    },
    6: {
        "title": "Tag queue",
        "action": tag_queue
    },
    7: {
        "title": "List queue tags",
        "action": list_queue_tags
    },
    8: {
        "title": "Untag queue",
        "action": untag_queue
    }
}


def main():
    client = boto3.client(
        'sqs', 
        aws_access_key_id=os.environ['ACCESS_KEY'],
        aws_secret_access_key=os.environ['SECRET_KEY']
    )

    print( f'{bcolors.HEADER}=================SQS Terminal Manager=================' )

    while ( True ):
        for option in menu_options:
            title = menu_options[ option ][ 'title' ]
            print( f'{bcolors.OKGREEN}{option} - {title}' )
        try:
            option = int(input(f'{bcolors.ENDC}Ingrese el número de la acción a ejecutar (ingrese 0 para salir): \n'))

            if option == 0:
                client.close()
                exit(0)        
            elif option > 0 and option <= len( menu_options ):
                menu_options[option]["action"](client)
            else:
                print('No es una opción válida, vuelva a intentar')
        except ValueError:
                print('No es una opción válida, vuelva a intentar')

if __name__ == "__main__":
    main()