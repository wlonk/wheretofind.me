from wheretofindme.forms import CustomUserForm


def test_CustomUserForm():
    """
    Test that init sets appropriate attributes.
    """
    form = CustomUserForm()
    assert hasattr(form, "helper")
    assert hasattr(form.helper, "layout")
