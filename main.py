from agents.coordinator import Coordinator
from config_loader import ConfigLoader

model = ConfigLoader().get_model()

coordinator = Coordinator(model, 'You will be debate coordinator, reply as short as possible')

response = coordinator.ask()

print(response)
