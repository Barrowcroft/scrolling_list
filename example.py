"""Example implementation of a CTkScrollingList."""

from typing import Callable

import customtkinter as ct

from scrolling_list.scrolling_list import CTkScrollingList, CTkScrollingListItemProtocol

# Because CustomTkinter has no stub file:
# pyright: reportUnknownMemberType = false
# pyright: reportMissingTypeStubs = false

ct.set_appearance_mode("dark")
ct.set_default_color_theme("blue")

NORMALCOLOUR = ("gray70", "gray24")
HIGHLIGHCOLOUR = ("gray60", "gray35")


class CTkScrollingListItem(
    ct.CTkFrame
):  # pylint: disable=too-many-ancestors, too-many-instance-attributes
    """
    The CTkScrollingListItem class.
    This is the layout used to display each list item.
    """

    def __init__(
        self,
        master: ct.CTkScrollableFrame,
        index: int,
        data: dict[str, str],
        item_selected_callback: Callable[[int], None],
    ) -> None:
        """Initialises the class."""

        super().__init__(master)

        self._item_selected_callback: Callable[[int], None] = item_selected_callback

        # Configure layout.

        self.configure(fg_color=NORMALCOLOUR)

        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)
        self.columnconfigure(index=0, weight=1)

        # Label showing the item text.

        _label = ct.CTkLabel(self, text=data["text"], height=25, anchor="w")
        _label.grid(row=0, column=0, padx=0, pady=0, sticky="we")

        # Connect callback for item selected.

        self._bind_callback(index)

    def _bind_callback(self, index: int) -> None:

        # Bind to main frame.

        self.bind("<Button-1>", lambda _, i=index: self._select_item(i))  # type: ignore

        # Bind to children.

        for _child in self.winfo_children():  # type: ignore
            _child.bind("<Button-1>", lambda _, i=index: self._select_item(i))  # type: ignore

    def _select_item(self, index: int) -> None:
        """The callbaclk for item selected."""

        self._item_selected_callback(index)


# These are the callback provided to the CTkScrollingList.


def list_item_requested(
    master: ct.CTkScrollableFrame,
    index: int,
    data: dict[str, str],
    callback: Callable[[int], None],
) -> CTkScrollingListItemProtocol:
    """Callback invoked to create a new list item."""
    return CTkScrollingListItem(master, index, data, callback)


def list_item_selected(index: int, data: dict[str, str]) -> bool:
    """Callback from CTkScrollingList invoked when a list item is selected."""
    print(f"Selected index: {index} {data}")
    return True


class App(ct.CTk):
    """Test app for CTkScrollableList."""

    def __init__(self):
        super().__init__()

        self.title("Selectable & Editable List")
        self.geometry("420x480")

        self.attributes("-topmost", True)
        self.resizable(False, False)

        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)

        self._list: CTkScrollingList = CTkScrollingList(
            self,
            "Scrollable List",
            list_item_requested,
            list_item_selected,
        )
        self._list.grid(row=0, column=0, padx=15, pady=15, sticky="nswe")
        self._list.add_item({"text": "Apple", "info": ""})
        self._list.add_item({"text": "Banana", "info": ""})
        self._list.add_item({"text": "Monkey", "info": ""})
        self._list.add_item({"text": "Blood Orange", "info": ""})
        self._list.delete_item(2)
        self._list.update_item(2, {"text": "Orange", "info": ""})
        self.mainloop()


if __name__ == "__main__":
    app = App()
