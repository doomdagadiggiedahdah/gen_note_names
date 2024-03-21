import ollama
import os
import subprocess
import sys
import re


def suggest_title_for_note_content(content):
    response = ollama.chat(model="mistral", messages=[
        {
        'role': 'user',
        'content': f"<text>{content}</text> Take this text and create a suitable title. It should contain no punctuation, be fewer than 10 words. Only return the title you suggest itself. DO NOT INCLUDE the following characters: '# ^ [ ] | / \ : '. Most importantly, have the title be action oriented, as if I would apply the note title in my life. ONLY INCLUDE ONE TITLE.",
        'options': {
            "temperature": 1
            }
        }
    ])
    return response['message']['content'].lstrip()

def get_untitled_notes(directory):
    untitled_notes = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if 'Untitled' in file:
                untitled_notes.append(os.path.join(root, file))
    return untitled_notes

def rename_file(old_path, new_name):
    new_path = os.path.join(os.path.dirname(old_path), new_name)
    os.rename(old_path, new_path)
    print(f"Renamed '{old_path}' to '{new_path}'")
    return new_path

def update_references_in_notes(directory, old_name, new_name):
    print(f"{old_name =  }")
    print(f"{new_name =  }")
    
    # Preparing the regex pattern to find the old_name within double brackets
    pattern = f"\\[\\[{old_name[:-3]}\\]\\]"
    print(f"{pattern = }")
    
    # Walking through the directory and its subdirectories to find all .md files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                # Reading the file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                if file_path == "/home/mat/Obsidian/ZettleKasten/Untitled 44.md":
                    #print(file_content)
                    print("this hsould only happen once")
                
                # Performing the search and replace
                updated_content = re.sub(pattern, f"[[{new_name}]]", file_content)
                #print("and here's the updated\n\n\n" + updated_content)
                
                # Only write back to file if changes were made
                if updated_content != file_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                        print(f"Updated references in '{file_path}' from '{old_name}' to '{new_name}'")

def main():
    notes_directory = "/home/mat/Obsidian/ZettleKasten/"
    untitled_notes = get_untitled_notes(notes_directory)

    for note_path in untitled_notes:
        with open(note_path, 'r', encoding='utf-8') as file:
            content = file.read()

        original_note_name = os.path.basename(note_path)
        print("######################################")
        print(f"Summarize / delete? {original_note_name}")
        print("######################################\n\n")
        print(content)

        next_action = input("\n\nPress 'n' to stop, 'delete' to remove, 's' to skip, or any key to generate: ")
        if next_action.lower() == 'n':
            break
        elif next_action.lower() == 's':
            continue
        elif next_action.lower() == 'delete':
            print(f"Deleting {original_note_name}\n\n")
            os.remove(note_path)
            continue

        while True:
            suggested_title = suggest_title_for_note_content(content) + ".md"
            print(f"Suggested title for note '{note_path}': {suggested_title}")
            
            user_input = input("Do you want to rename or regenerate this file? [y/r/n]: ")
            if user_input.lower() == 'y':
                new_path = rename_file(note_path, suggested_title)
                new_note_name = os.path.basename(new_path)
                update_references_in_notes(notes_directory, original_note_name, new_note_name)
                break
            elif user_input.lower() == 'r':
                feedback = input("Tell what you didn't like about this title: ")
                content = f"{content}\n\nFeedback on previous title: '{suggested_title[:-3]}' was that {feedback}. Please regenerate another title with the following instructions. "
                continue
            elif user_input.lower() == 'n':
                break


if __name__ == "__main__":
    main()

## prompt engineering needs work, getting titles that don't follow the rules and that's frustrating.
