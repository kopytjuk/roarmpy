
def test_import():
    import roarmpy  # noqa


def test_output_version():
    from roarmpy import __version__
    assert isinstance(__version__, str)
