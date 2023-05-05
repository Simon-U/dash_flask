from flask_admin.base import BaseView
from flask_admin.actions import ActionsMixin
from flask_admin import form, helpers
import platform


class BaseFileAdmin(BaseView, ActionsMixin):
    can_upload = True
    """
        Is file upload allowed.
    """

    can_download = True
    """
        Is file download allowed.
    """

    can_delete = True
    """
        Is file deletion allowed.
    """

    can_delete_dirs = True
    """
        Is recursive directory deletion is allowed.
    """

    can_mkdir = False
    """
        Is directory creation allowed.
    """

    can_rename = True
    """
        Is file and directory renaming allowed.
    """

    allowed_extensions = None
    """
        List of allowed extensions for uploads, in lower case.

        Example::

            class MyAdmin(FileAdmin):
                allowed_extensions = ('swf', 'jpg', 'gif', 'png')
    """

    editable_extensions = tuple()
    """
        List of editable extensions, in lower case.

        Example::

            class MyAdmin(FileAdmin):
                editable_extensions = ('md', 'html', 'txt')
    """

    list_template = "admin/file/list.html"
    """
        File list template
    """

    upload_template = "admin/file/form.html"
    """
        File upload template
    """

    upload_modal_template = "admin/file/modals/form.html"
    """
        File upload template for modal dialog
    """

    mkdir_template = "admin/file/form.html"
    """
        Directory creation (mkdir) template
    """

    mkdir_modal_template = "admin/file/modals/form.html"
    """
        Directory creation (mkdir) template for modal dialog
    """

    rename_template = "admin/file/form.html"
    """
        Rename template
    """

    rename_modal_template = "admin/file/modals/form.html"
    """
        Rename template for modal dialog
    """

    edit_template = "admin/file/form.html"
    """
        Edit template
    """

    edit_modal_template = "admin/file/modals/form.html"
    """
        Edit template for modal dialog
    """

    form_base_class = form.BaseForm
    """
        Base form class. Will be used to create the upload, rename, edit, and delete form.

        Allows enabling CSRF validation and useful if you want to have custom
        constructor or override some fields.

        Example::

            class MyBaseForm(Form):
                def do_something(self):
                    pass

            class MyAdmin(FileAdmin):
                form_base_class = MyBaseForm

    """

    # Modals
    rename_modal = False
    """Setting this to true will display the rename view as a modal dialog."""

    upload_modal = False
    """Setting this to true will display the upload view as a modal dialog."""

    mkdir_modal = False
    """Setting this to true will display the mkdir view as a modal dialog."""

    edit_modal = False
    """Setting this to true will display the edit view as a modal dialog."""

    # List view
    possible_columns = "name", "rel_path", "is_dir", "size", "date"
    """A list of possible columns to display."""

    column_list = "name", "size", "date"
    """A list of columns to display."""

    column_sortable_list = column_list
    """A list of sortable columns."""

    default_sort_column = None
    """The default sort column."""

    default_desc = 0
    """The default desc value."""

    column_labels = dict((column, column.capitalize()) for column in column_list)
    """A dict from column names to their labels."""

    date_format = "%Y-%m-%d %H:%M:%S"
    """Date column display format."""

    def __init__(
        self,
        base_url=None,
        name=None,
        category=None,
        endpoint=None,
        url=None,
        verify_path=True,
        menu_class_name=None,
        menu_icon_type=None,
        menu_icon_value=None,
        storage=None,
        can_mkdir=True,
    ):
        """
        Constructor.

        :param base_url:
            Base URL for the files
        :param name:
            Name of this view. If not provided, will default to the class name.
        :param category:
            View category
        :param endpoint:
            Endpoint name for the view
        :param url:
            URL for view
        :param verify_path:
            Verify if path exists. If set to `True` and path does not exist
            will raise an exception.
        :param storage:
            The storage backend that the `BaseFileAdmin` will use to operate on the files.
        """
        self.base_url = base_url
        self.storage = storage

        self.init_actions()

        self._on_windows = platform.system() == "Windows"

        # Convert allowed_extensions to set for quick validation
        if self.allowed_extensions and not isinstance(self.allowed_extensions, set):
            self.allowed_extensions = set(self.allowed_extensions)

        # Convert editable_extensions to set for quick validation
        if self.editable_extensions and not isinstance(self.editable_extensions, set):
            self.editable_extensions = set(self.editable_extensions)

        super(BaseFileAdmin, self).__init__(
            name,
            category,
            endpoint,
            url,
            menu_class_name=menu_class_name,
            menu_icon_type=menu_icon_type,
            menu_icon_value=menu_icon_value,
        )
