# An example of Composite design pattern on
# folders and files.
#
# WIP
#######################################
import abc


class Node(abc.ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self.parent: "Folder | None" = None

    def move(self, new_folder: "Folder") -> None:
        previous = self.parent
        new_folder.add_child(self)
        if previous:
            del previous.children[self.name]

    @abc.abstractmethod
    def copy(self, new_folder: "Folder") -> None: ...

    @abc.abstractmethod
    def remove(self) -> None: ...


class Folder(Node):
    def __init__(self, name: str, children: dict[str, Node] | None = None) -> None:
        super().__init__(name)
        self.children = children or {}

    def __repr__(self) -> str:
        return f"Folder({self.name!r}, {self.children!r})"

    def add_child(self, node: Node) -> Node:
        node.parent = self
        return self.children.setdefault(node.name, node)

    def copy(self, new_folder: "Folder") -> None:
        target = new_folder.add_child(Folder(self.name))
        assert isinstance(target, Folder)
        for child in self.children:
            self.children[child].copy(target)

    def remove(self) -> None:
        names = list(self.children)
        for name in names:
            self.children[name].remove()
        if self.parent:
            del self.parent.children[self.name]


class File(Node):
    def __repr__(self) -> str:
        return f"File({self.name!r})"

    def copy(self, new_folder: Folder) -> None:
        new_folder.add_child(File(self.name))

    def remove(self) -> None:
        if self.parent:
            del self.parent.children[self.name]
