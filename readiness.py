import json

def calculate_posture_increment(stats):
    base_increment = 10
    footwork_bonus = max(0, (stats['Footwork'] - 5) * 1)
    agility_bonus = max(0, (stats['Agility'] - 5) * 0.5)
    skill_bonus = (stats['Skill'] - 5) * 0.25  # Can be negative
    stamina_penalty = 0
    if stats['Stamina'] < 50:
        stamina_penalty = 0.10  # 10% reduction
    total_increment = base_increment + footwork_bonus + agility_bonus + skill_bonus
    total_increment *= (1 - stamina_penalty)
    return total_increment

def load_characters(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    characters = {}
    for char_name, stats in data.items():
        stats['Posture'] = 0
        stats['Increment'] = calculate_posture_increment(stats)
        characters[char_name] = stats
    return characters

def next_turn(characters):
    for stats in characters.values():
        stats['Posture'] += stats['Increment']

def get_next_actor(characters):
    eligible_chars = {name: stats for name, stats in characters.items() if stats['Posture'] >= 75}
    if not eligible_chars:
        return None
    # Return the character with the highest posture
    return max(eligible_chars.items(), key=lambda x: x[1]['Posture'])[0]

def main():
    characters = load_characters('characters.json')
    turn = 0
    while True:
        user_input = input('Press "Enter" to advance turn or enter character name for reaction: ').strip()
        if user_input == '':
            turn += 1
            next_turn(characters)
            print(f'\n--- Turn {turn} ---')
            for name, stats in characters.items():
                print(f"{name}'s Posture: {stats['Posture']:.2f}")
            next_actor = get_next_actor(characters)
            if next_actor:
                print(f"\n{next_actor} can act now!")
                characters[next_actor]['Posture'] = 0  # Reset posture after action
        else:
            # Reaction
            if user_input in characters and characters[user_input]['Posture'] >= 75:
                print(f"\n{user_input} reacts and acts now!")
                characters[user_input]['Posture'] = 0  # Reset posture after action
            else:
                print(f"\n{user_input} cannot act now.")
                
# Run the main function
if __name__ == '__main__':
    main()
