
class Reach:
    def __init__(self, username, email, subject, campaign):
        """
        Initialize reach details including campaign tracking.

        :param username: Recipient's name.
        :param email: Recipient's email.
        :param subject: Email subject.
        :param campaign: An instance of the Campaign class.
        """
        self.username = username
        self.email = email
        self.subject = subject
        self.campaign = campaign
        self.step = 1  # Default start at step 1

    def get_current(self):
        """Fetch the current email content from the campaign."""
        return self.campaign.get_step_content(self.step)

    def proceed(self):
        """Advance to the next step in the campaign."""
        self.step += 1
        print(f"📩 Progressed to step {self.step} in '{self.campaign.name}' campaign.")

    def __repr__(self):
        return f"Reach(username={self.username}, email={self.email}, subject={self.subject}, campaign_name={self.campaign.name}, step={self.step})"