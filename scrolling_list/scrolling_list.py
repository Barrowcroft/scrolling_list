"""CTkScrollingList - Implementation of a list control using CustomTkinter's scrolling frame."""

from typing import Any, Callable, Optional, Protocol

import customtkinter as ct

# Because CustomTkinter has no stub file:
# pyright: reportUnknownMemberType = false
# pyright: reportMissingTypeStubs = false

ct.set_appearance_mode("dark")
ct.set_default_color_theme("blue")

NORMALCOLOUR = ("gray70", "gray24")
HIGHLIGHCOLOUR = ("gray60", "gray35")


class CTkScrollingListItemProtocol(Protocol):
    """
    The CTkScrollingListItemProtocol defines what is expected to
    be created and passed to the CTkScrollingList.

    The 'item_selected_callback' is provided by the CTkScrollingList
    to enable the CTkScrollingListItemProtocol to notify it when
    it has been selected.
    """

    _item_selected_callback: Callable[[int], None]

    def __init__(
        self,
        master: ct.CTkScrollableFrame,
        index: int,
        data: dict[str, str],
        item_selected_callback: Callable[[int], None],
    ) -> None: ...
    def _bind_callback(self, index: int) -> None: ...
    def _select_item(self, index: int) -> None: ...

    # For the sake of type checking.

    def pack(self, *args: Any, **kwargs: Any):
        """Stub for CustomTkinter method."""

    def destroy(self):
        """Stub for CustomTkinter method."""

    def configure(self, *args: Any, **kwargs: Any):
        """Stub for CustomTkinter method."""


class CTkScrollingList(
    ct.CTkFrame
):  # pylint: disable=too-many-ancestors, too-many-instance-attributes
    """
    The CTkScrollingList class.

    The 'list_item_creation_callback' is invoked by CTkScrollingList to
    request the calling program to supply a new list item that adheres to the
    CTkScrollingListItem protocal.

    The 'list_item_selected_callback' is invoked by CTkScrollingList to
    inform the calling program that a list item has been selected.
    """

    def __init__(
        self,
        master: ct.CTk,
        title: str,
        list_item_request_callback: Callable[
            [ct.CTkScrollableFrame, int, dict[str, str], Callable[[int], None]],
            CTkScrollingListItemProtocol,
        ],
        list_item_selected_callback: Callable[[int, dict[str, str]], bool],
    ):
        """Initialises the class."""

        super().__init__(master)

        self.list_item_request_callback: Callable[
            [ct.CTkScrollableFrame, int, dict[str, str], Callable[[int], None]],
            CTkScrollingListItemProtocol,
        ] = list_item_request_callback
        self._list_item_selected_callback: Callable[[int, dict[str, str]], bool] = (
            list_item_selected_callback
        )

        # Configure base frame.

        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)

        # Create and configure scrollable frame.

        self._scrollable_frame: ct.CTkScrollableFrame = ct.CTkScrollableFrame(
            self, label_text=title, label_fg_color=NORMALCOLOUR
        )
        self._scrollable_frame.rowconfigure(index=0, weight=1)
        self._scrollable_frame.columnconfigure(index=0, weight=1)
        self._scrollable_frame._label.grid_configure(padx=0, pady=0)  # type: ignore

        # Add scrollable frame to main frame.

        self._scrollable_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")

        # Initialse other.

        self._items: list[dict[str, str]] = []
        self._item_index: Optional[int] = None
        self._item_widgets: list[CTkScrollingListItemProtocol] = []

        # Display the list.

        self._display_list()

    def _display_list(self):
        """Display the list items."""

        # Clear the current list display.

        for _widget in self._item_widgets:
            _widget.destroy()

        self._item_widgets.clear()

        # Process the _items to create entries in _item_widgets,
        # and create those widgets in the _scrolling_frame.

        for _index, _item_data in enumerate(self._items):

            # Create the item widget and add it to the list.

            _item: CTkScrollingListItemProtocol = self.list_item_request_callback(
                self._scrollable_frame,
                _index,
                _item_data,
                self._select_item,
            )
            _item.pack(fill="x", pady=(0, 1), padx=0)

            self._item_widgets.append(_item)
            self._item_index = None

            # Scroll to the bottom of the list.

            self._scrollable_frame._parent_canvas.update_idletasks()  # pylint: disable=protected-access  # type: ignore
            self._scrollable_frame._parent_canvas.yview_moveto(  # pylint: disable=protected-access  # type: ignore
                1
            )

    def add_item(self, data: dict[str, str]):
        """Adds an item to the items list."""
        self._items.append(data)
        self._display_list()

    def update_item(self, index: int, data: dict[str, str]):
        """Updates an item from the items list."""
        self._items[index] = data
        self._display_list()

    def delete_item(self, index: int):
        """Deletes an item from the items list."""
        self._items.pop(index)
        self._display_list()

    def _select_item(self, index: int):
        """Select an item."""
        if self._list_item_selected_callback(index, self._items[index]):
            self._item_index = index
            self._update_selection_highlight()

    def _update_selection_highlight(self):
        """Change background color of selected item."""
        for _index, _frame in enumerate(self._item_widgets):
            if _index == self._item_index:
                _frame.configure(fg_color=HIGHLIGHCOLOUR)
            else:
                _frame.configure(fg_color=NORMALCOLOUR)
