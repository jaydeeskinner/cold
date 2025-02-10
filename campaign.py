import os
import json

class Campaign:
	CAMPAIGNS_FOLDER = "campaigns"
	os.makedirs(CAMPAIGNS_FOLDER, exist_ok=True)

	@classmethod
	def load_campaigns(cls):
		"""Load all campaign JSON files from the campaigns folder."""
		campaigns = []
		for filename in os.listdir(cls.CAMPAIGNS_FOLDER):
			if filename.endswith(".json"):
				with open(os.path.join(cls.CAMPAIGNS_FOLDER, filename), "r") as file:
					try:
						data = json.load(file)
						campaigns.append(cls(data["name"], data["steps"]))
					except (json.JSONDecodeError, KeyError):
						print(f"Skipping invalid file: {filename}")
		return campaigns

	def __init__(self, name, steps):
		self.name = name
		self.steps = steps
		self.save()

	def save(self):
		"""Save the campaign as a JSON file."""
		with open(os.path.join(self.CAMPAIGNS_FOLDER, f"{self.name}.json"), "w") as file:
			json.dump({"name": self.name, "steps": self.steps}, file, indent=4)

	def get_step_content(self, step):
		return self.steps[min(step - 1, len(self.steps) - 1)]

loaded_campaigns = Campaign.load_campaigns()
