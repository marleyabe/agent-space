import redis
import datetime
import time
import threading

class Chat_Agent:
    def __init__(self, name: str, time_wait: int = 5, phone: str = 'mockup'):
        self.name = name
        self.time_wait = time_wait
        self.mensages = ''
        self.phone = phone

        # Redis
        self.redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

        self.redis_key = f"buffer:{self.phone}"
        self.redis_key_timer = f"buffer_timer:{self.phone}"


    def receive_message(self, message):
        
        thread1 = threading.Thread(target=self.__buffer, args=(message,))
        thread1.start()

        thread2 = threading.Thread(target=self.__wait_buffer)
        thread2.start()

        
        return self.mensages
    
    def __wait_buffer(self):

        while True:
            if len(self.redis.lrange(self.redis_key, 0, -1) ) > 0:
                time.sleep(self.time_wait)
                if not self.redis.exists(self.redis_key_timer):
                    self.mensages = self.redis.lrange(self.redis_key, 0, -1)
                    self.redis.delete(self.redis_key)
                    print(f"Buffer expirado para {self.phone}, mensagens processadas: {self.mensages}")
                    break
            break
                    
    
    def __buffer(self, message: str):

        self.redis.set(self.redis_key_timer, '1', ex=self.time_wait)
        self.redis.rpush(self.redis_key, message)

        print(f"{self.phone}: {self.redis.lrange(self.redis_key, 0, -1)}")
        
        
    def process_message(self):

        pass


    def send_message(self):

        print(f"Enviando mensagem para {self.phone}: {self.mensages}")
        return 0
    
    def destroy_buffer(self):

        self.redis.delete(self.redis_key)
        self.redis.delete(self.redis_key_timer)

        print(f"Buffer destruído para {self.phone}")

if __name__ == "__main__":
    agent = Chat_Agent(name="ChatAgent", time_wait=5, phone="mockup")

    print("Digite uma mensagem (ou 'sair' para encerrar):")
    while True:
        user_input = input()
        if user_input.lower() == 'sair':
            break
        agent.receive_message(user_input)
    agent.destroy_buffer()