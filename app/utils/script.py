class Text:
    @staticmethod
    def remove_indentation(text):
        """Remove leading whitespace from each line in the provided text."""
        # Split the text into lines
        lines = text.splitlines()
        
        # Remove leading whitespace (spaces or tabs) from each line
        lines_no_indent = [line.lstrip() for line in lines]
        
        # Join the lines back into a single string
        return "\n".join(lines_no_indent)
