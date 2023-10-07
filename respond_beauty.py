def make_it_beautiful(respond: str):
    """
    If you use custom HTML template in your responses, you will need to use this function.
    Otherwise, you will get a lot of problems with your HTML code.

    """
    respond = respond.strip()
    respond = respond.replace('\n', '<br>')
    s = respond.split('```')
    return '\n\n```\n\n'.join(s)
