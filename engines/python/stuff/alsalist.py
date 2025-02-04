import alsaaudio

# Get a list of available sound cards
cards = alsaaudio.cards()

print("Available ALSA sound cards:")
for index, card in enumerate(cards):
    print(f"{index}: {card}")

