def make_it_beautiful(respond: str):
    respond = respond.strip()
    s = respond.split('```')
    return '\n\n```\n\n'.join(s)
