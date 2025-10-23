import time
import threading
from pynput import keyboard
import sys # Import sys for console output manipulation

# Global flag to control the F5/Enter loop
running = False
# Thread object for the F5/Enter loop
press_thread = None
# Time when the automation started
start_time = None

def press_f5_and_enter():
    global running, start_time
    controller = keyboard.Controller()
    is_f5_turn = False # Flag to alternate between F5 and Enter

    while running:
        key_pressed_display = ""
        if is_f5_turn:
            # Press F5
            controller.press(keyboard.Key.f5)
            controller.release(keyboard.Key.f5)
            key_pressed_display = "F5"
        else:
            # Press Enter
            controller.press(keyboard.Key.enter)
            controller.release(keyboard.Key.enter)
            key_pressed_display = "Enter"

        is_f5_turn = not is_f5_turn # Toggle the flag for the next turn

        # Calculate elapsed time
        if start_time:
            elapsed_seconds = int(time.time() - start_time)
            hours, remainder = divmod(elapsed_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            time_str = "00:00:00"

        # Output to console using carriage return to overwrite the line
        sys.stdout.write(f"\rRunning Time: {time_str} | Last Pressed: {key_pressed_display}      ")
        sys.stdout.flush() # Ensure the output is immediately written to the console

        time.sleep(1) # Wait for 1 seconds before the next key press

def on_press(key):
    global running, press_thread, start_time
    try:
        if key == keyboard.Key.f1:
            if not running:
                print("\nF1 pressed: Starting F5/Enter automation.")
                running = True
                start_time = time.time() # Record start time
                # Clear the previous line and start fresh display
                sys.stdout.write("\r                                                                 ")
                sys.stdout.flush()
                press_thread = threading.Thread(target=press_f5_and_enter)
                press_thread.start()
            else:
                print("\nF1 pressed: Stopping F5/Enter automation.")
                running = False
                start_time = None # Reset start time
                # Give the thread a moment to recognize the stop signal
                time.sleep(0.1)
                if press_thread and press_thread.is_alive():
                    # Wait for the thread to finish its current 5-sec cycle
                    press_thread.join(timeout=6)
                # Clear the console line after stopping
                sys.stdout.write("\rAutomation Stopped.                                               \n")
                sys.stdout.flush()

    except AttributeError:
        # This block handles special keys (like F1, F2, etc.) vs. character keys
        pass

def main():
    print("DJMAX Clear Pass Auto-Farmer                   \n")
    print("~~~Instructions~~~                   \n")
    print("1. Create a private mutiplayer lobby with password so that no one will enter and interrupt your automation.")
    print("2. Set your key mode to OBSERVE")
    print("3. Select your preferred song. Recommend is Put Em Up as it is the shortest song in the game.")
    print("4. Press F1 to Start the F5 and Enter automation.")
    print("5. Go do something else while it does the magic. Unfortunately, you cannot do anything else on your PC.")
    print("6. Press F1 again to Stop the F5 and Enter automation.")
    print("7. Close this app if you don't need it for the session. eksdee")
    print("Listening for key presses...")
    # Set up the listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()