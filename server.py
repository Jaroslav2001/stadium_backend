if __name__ == '__main__':
    import uvicorn
    from setting import setting
    uvicorn.run('main:app', **setting.SERVER)
