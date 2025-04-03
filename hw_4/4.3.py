import multiprocessing
import time
import codecs
from datetime import datetime

def process_a(queue_a, queue_b):
    while True:
        message = queue_a.get()
        if message is None:
            break
        processed_message = message.lower()
        time.sleep(5)
        queue_b.put(processed_message)

def process_b(queue_b, queue_main):
    while True:
        message = queue_b.get()
        if message is None:
            break
        encoded_message = codecs.encode(message, 'rot_13')
        print(f"{datetime.now()}: {encoded_message}")
        queue_main.put(encoded_message)

def main():
    queue_a = multiprocessing.Queue()
    queue_b = multiprocessing.Queue()
    queue_main = multiprocessing.Queue()

    process_a_instance = multiprocessing.Process(target=process_a, args=(queue_a, queue_b))
    process_b_instance = multiprocessing.Process(target=process_b, args=(queue_b, queue_main))

    process_a_instance.start()
    process_b_instance.start()

    try:
        while True:
            message = input("Введите сообщение: ")
            queue_a.put(message)
            if message.lower() == 'exit':
                break
    finally:
        queue_a.put(None)
        queue_b.put(None)
        process_a_instance.join()
        process_b_instance.join()

if __name__ == "__main__":
    main()