# pylint: skip-file

"""CTkScrollingList - Type stub for a list control using CustomTkinter's scrolling frame."""

from typing import Any, Callable, Optional, Protocol

import customtkinter as ct

# pyright: reportUnknownMemberType = false
# pyright: reportMissingTypeStubs = false

NORMALCOLOUR: tuple[str, str]
HIGHLIGHCOLOUR: tuple[str, str]

class CTkScrollingListItemProtocol(Protocol):
    """Protocol describing an item for CTkScrollingList."""

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
    def pack(self, *args: Any, **kwargs: Any) -> Any: ...
    def destroy(self) -> Any: ...
    def configure(self, *args: Any, **kwargs: Any) -> Any: ...

class CTkScrollingList(ct.CTkFrame):
    """A scrollable list control using CustomTkinter."""

    list_item_request_callback: Callable[
        [ct.CTkScrollableFrame, int, dict[str, str], Callable[[int], None]],
        CTkScrollingListItemProtocol,
    ]
    _list_item_selected_callback: Callable[[int, dict[str, str]], bool]
    _scrollable_frame: ct.CTkScrollableFrame
    _items: list[dict[str, str]]
    _item_index: Optional[int]
    _item_widgets: list[CTkScrollingListItemProtocol]

    def __init__(
        self,
        master: ct.CTk,
        title: str,
        list_item_request_callback: Callable[
            [ct.CTkScrollableFrame, int, dict[str, str], Callable[[int], None]],
            CTkScrollingListItemProtocol,
        ],
        list_item_selected_callback: Callable[[int, dict[str, str]], bool],
    ) -> None: ...
    def _display_list(self) -> None: ...
    def add_item(self, data: dict[str, str]) -> None: ...
    def update_item(self, index: int, data: dict[str, str]) -> None: ...
    def delete_item(self, index: int) -> None: ...
    def _select_item(self, index: int) -> None: ...
    def _update_selection_highlight(self) -> None: ...
