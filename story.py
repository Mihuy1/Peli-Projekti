import textwrap

story = '''The long-awaited summer has arrived!
For a year, you've been saving money to travel.
You couldn't leave your beloved pet alone, so you took it with you.
At the airport, as you boarded the plane, you had to leave it in the cargo hold.
But upon landing, to your horror, you realized that your pet was on a different flight.
Due to an error, it was sent on another flight at the same time.
Now you have to find it as quickly as possible, even if it means using all your vacation savings.'''

wrapper = textwrap.TextWrapper(width=80, break_long_words=False, replace_whitespace=False)
word_list = wrapper.wrap(text=story)


def getStory():
    return word_list
