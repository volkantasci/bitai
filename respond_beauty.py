def make_it_beautiful(respond: str):
    respond = respond.strip()
    respond = respond.replace('\n', '<br>')
    s = respond.split('```')
    return '\n\n```\n\n'.join(s)
