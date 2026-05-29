from vitalis.src.brain.brain_interface import VitalisBrain

def main():
    brain = VitalisBrain()
    brain.load_brain()
    
    print("FSI Core Active. Type your prompt (or 'exit' to save and quit):")
    while True:
        user_input = input(">> ")
        if user_input.lower() == 'exit':
            brain.save_brain()
            break
        
        # We pass the input to the brain
        # The logic gate is handled automatically by the brain's pulse/generate logic
        response = brain.generate_response(user_input, "General Intelligence Interface")
        print(f"FSI: {response}")

if __name__ == "__main__":
    main()
