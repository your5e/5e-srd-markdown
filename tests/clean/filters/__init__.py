class TestFilter:
    def run_text_through_filter(self, filter, text):
        lines = text.splitlines()

        # Use the same restart logic as clean_srd to handle line count changes
        last_index = -1
        while True:
            result = None
            for index in range(len(lines)):
                if index <= last_index:
                    continue

                result = filter(lines, index)
                if result is not None:
                    last_index = index + result
                    break

            if result is None:
                break

        result = '\n'.join(lines)
        if text.endswith('\n'):
            result += '\n'
        return result
