class TestFilter:
    def run_text_through_processor(self, processor, text, filename='test'):
        lines = text.splitlines()

        last_index = -1
        while True:
            result = None
            for index in range(len(lines)):
                if index <= last_index:
                    continue

                result = processor(lines, index, filename)
                if result is not None:
                    last_index = index + result
                    if result != 0:
                        break

            if result is None:
                break

        result = '\n'.join(lines)
        if text.endswith('\n'):
            result += '\n'
        return result
