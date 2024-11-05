import random
import time
from threading import Thread, Lock
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(Thread):
    def __init__(self, name, cafe):
        super().__init__()
        self.name = name
        self.cafe = cafe

    def run(self):
        wait_time = random.randint(3, 10)
        time.sleep(wait_time)
        self.cafe.guest_arrival(self)

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables
        self.lock = Lock()

    def guest_arrival(self, guest):
        self.queue.put(guest)
        print(f"{guest.name} прибыл в кафе и стал в очередь.")

    def discuss_guests(self):
        while True:
            try:
                guest = self.queue.get(timeout=5)  # Ждем 5 секунд
                self.seat_guest(guest)
            except Exception as e:
                print("Нет больше гостей для обслуживания.")
                break

    def seat_guest(self, guest):
        with self.lock:
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    print(f"{guest.name} сел за стол {table.number}.")
                    time.sleep(2)
                    table.guest = None
                    print(f"{guest.name} покинул стол {table.number}.")
                    break


cafe = Cafe(Table(1), Table(2), Table(3))

servicing_thread = Thread(target=cafe.discuss_guests)
servicing_thread.start()


for guests_names in [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]:
    guest = Guest(guests_names, cafe)
    guest.start()