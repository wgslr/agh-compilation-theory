Dla uniknięcia pisania metody printTree w każdej klasie, można je zgrupować
przez użycie dekoratora:

```python
class TreePrinter:

  @addToClass(BinExpr)
  def printTree(node):
    "do something"

  @addToClass(UnaryExpr)
  def printTree(node):
    "do something"
```

