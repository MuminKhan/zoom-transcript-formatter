import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please specify the raw transcript path.")
        exit(-1)

    transcript_path = sys.argv[1]
    transcript = {}

    with open(transcript_path) as f:
        change_speaker = False
        current_speaker = None
        current_time = None
        collected_text = []

        for line_number, line in enumerate(f):
            line = line.strip()
            if 'user avatar' in line:
                # signal a user change
                change_speaker = True
            elif change_speaker:
                # write old speaker block
                if len(collected_text) > 0:
                    session_text = '. '.join([text for _, text in collected_text]).replace('..', '.')
                    transcript[collected_text[0][0]] = f'{current_speaker}: {session_text}'

                # reset info for new speaker block
                change_speaker = False
                current_speaker = line
                current_time = None
                collected_text = []
            elif ':' in line:
                # new timestamp
                current_time = line
            else:
                # collect timestamp + text
                collected_text.append((current_time, line))

    # basic output
    output_path = 'cleaned_'+transcript_path
    print(f'{transcript_path} ----> {output_path}')
    with open(output_path, 'w') as w:
        for k, v in transcript.items():
            w.write(f'{k} {v}\n')
