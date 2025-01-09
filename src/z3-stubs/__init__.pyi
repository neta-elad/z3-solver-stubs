from typing import (
    Any,
    Iterable,
    Sequence,
    TypeGuard,
    TypeVar,
)

class Context: ...
class Z3PPObject: ...

class Z3Exception(Exception):
    value: bytes

class AstRef(Z3PPObject):
    def eq(self, other: Any) -> bool: ...

class SortRef(AstRef):
    def name(self) -> str: ...
    def kind(self) -> int: ...

class BoolSortRef(SortRef): ...
class ArithSortRef(SortRef): ...
class DatatypeSortRef(SortRef): ...

class ArraySortRef(SortRef):
    def domain(self) -> SortRef: ...
    def range(self) -> SortRef: ...

class DatatypeRef(ExprRef):
    def sort(self) -> DatatypeSortRef: ...

class Datatype:
    def __init__(self, name: str, ctx: Context = ...) -> None: ...
    def create(self) -> DatatypeSortRef: ...
    def declare(self, name: str, *args: tuple[str, Datatype | SortRef]) -> None: ...

def CreateDatatypes(*ds: Datatype) -> list[DatatypeSortRef]: ...

class FuncDeclRef(AstRef):
    def __call__(self, *args: ExprRef) -> ExprRef: ...
    def arity(self) -> int: ...
    def domain(self, i: int) -> SortRef: ...
    def range(self) -> SortRef: ...
    def name(self) -> str: ...
    def kind(self) -> int: ...

class RecFunction(FuncDeclRef):
    def __init__(self, name: str, *sig: SortRef) -> None: ...

class ExprRef(AstRef):
    def children(self) -> list[ExprRef]: ...
    def __eq__(self, other) -> "BoolRef": ...  # type: ignore
    def __ne__(self, other) -> "BoolRef": ...  # type: ignore
    def decl(self) -> FuncDeclRef: ...
    def sort(self) -> SortRef: ...
    def sexpr(self) -> str: ...
    def num_args(self) -> int: ...
    def arg(self, i: int) -> "ExprRef": ...
    def translate(self, ctx: Context) -> "ExprRef": ...

class BoolRef(ExprRef): ...

class ArithRef(ExprRef):
    def __ge__(self, other: int) -> BoolRef: ...
    def __gt__(self, other: Any) -> BoolRef: ...
    def __le__(self, other: Any) -> BoolRef: ...
    def __lt__(self, other: Any) -> BoolRef: ...
    def __add__(self, other: int | ArithRef) -> ArithRef: ...
    def __sub__(self, other: int | ArithRef) -> ArithRef: ...
    def __mul__(self, other: int | ArithRef) -> ArithRef: ...
    def __mod__(self, other: int | ArithRef) -> ArithRef: ...
    def __truediv__(self, other: int | ArithRef) -> ArithRef: ...
    def __neg__(self) -> ArithRef: ...

class ArrayRef(ExprRef):
    def sort(self) -> ArraySortRef: ...
    def __getitem__(self, item: ExprRef) -> ExprRef: ...

class Const(ExprRef):
    def __init__(self, name: str, sort: SortRef): ...
    def decl(self) -> FuncDeclRef: ...

class IntNumRef(Const, ArithRef):
    def as_long(self) -> int: ...

class QuantifierRef(BoolRef):
    def num_vars(self) -> int: ...
    def var_sort(self, idx: int) -> SortRef: ...
    def var_name(self, idx: int) -> str: ...
    def is_forall(self) -> bool: ...
    def is_exists(self) -> bool: ...
    def body(self) -> BoolRef: ...
    def get_id(self) -> int: ...
    def qid(self) -> str: ...

class CheckSatResult: ...

class ModelRef(Z3PPObject):
    def get_sort(self, index: int) -> SortRef: ...
    def sorts(self) -> list[SortRef]: ...
    def get_universe(self, sort: SortRef) -> list[Const]: ...
    def decls(self) -> list[FuncDeclRef]: ...
    def eval(self, t: AnyExprRef, model_completion: bool = False) -> AnyExprRef: ...
    def sexpr(self) -> str: ...
    def __getitem__(self, t: AnyExprRef) -> AnyExprRef: ...

class Solver:
    def __init__(self, *, ctx: Context = ...) -> None: ...
    def check(self, *assumptions: Iterable[ExprRef] | ExprRef) -> CheckSatResult: ...
    def model(self) -> ModelRef: ...
    def reason_unknown(self) -> str: ...
    def set(self, *args: Any, **kwargs: Any) -> None: ...
    def from_file(self, filename: str) -> None: ...
    def from_string(self, string: str) -> None: ...
    def assertions(self) -> Sequence[BoolRef]: ...
    def unsat_core(self) -> Sequence[BoolRef]: ...
    def reset(self) -> None: ...
    def assert_exprs(self, *args: BoolRef) -> None: ...
    def add(self, arg: BoolRef) -> None: ...
    def to_smt2(self) -> str: ...
    def sexpr(self) -> str: ...
    def push(self) -> None: ...
    def pop(self) -> None: ...

def SolverFor(logic: str) -> Solver: ...

class Optimize(Solver):
    def add_soft(self, arg: BoolRef) -> None: ...

class ApplyResult(Z3PPObject):
    def as_expr(self) -> ExprRef: ...

class Tactic:
    def __init__(self, name: str, ctx: Context = ...): ...
    def __call__(
        self, goal: ExprRef, *arguments: Any, **keywords: Any
    ) -> ApplyResult: ...
    def solver(self) -> Solver: ...

AnyExprRef = TypeVar("AnyExprRef", bound=ExprRef)

def DeclareSort(name: str, ctx: Context = ...) -> SortRef: ...
def EnumSort(
    name: str, values: list[str], ctx: Context = ...
) -> tuple[SortRef, list[Const]]: ...
def ArraySort(domain: SortRef, range: SortRef) -> ArraySortRef: ...
def FreshConst(sort: SortRef, prefix: str = "") -> Const: ...
def Consts(names: str, sort: SortRef) -> tuple[Const, ...]: ...
def Function(name: str, *sig: SortRef) -> FuncDeclRef: ...
def RecAddDefinition(
    f: RecFunction, args: Const | list[Const], body: ExprRef
) -> None: ...
def FreshFunction(*sig: SortRef) -> FuncDeclRef: ...
def BoolSort(ctx: Context = ...) -> BoolSortRef: ...
def IntSort(ctx: Context = ...) -> ArithSortRef: ...

class Int(IntNumRef, Const):
    def __init__(self, name: str, ctx: Context = ...) -> None: ...

class Array(ArrayRef, Const):
    def __init__(self, name: str, domain: SortRef, range: SortRef) -> None: ...

def Store(array: ArrayRef, key: ExprRef, value: ExprRef) -> ArrayRef: ...
def FreshInt(prefix: str = "") -> Int: ...
def Ints(names: str, ctx: Context = ...) -> list[Int]: ...
def IntVal(val: int, ctx: Context = ...) -> IntNumRef: ...
def K(sort: SortRef, value: Any) -> ArrayRef: ...

class Bool(BoolRef, Const):
    def __init__(self, name: str, ctx: Context = ...) -> None: ...

def BoolVal(val: bool, ctx: Context = ...) -> BoolRef: ...
def If(a: BoolRef, b: AnyExprRef, c: AnyExprRef, ctx: Context = ...) -> AnyExprRef: ...
def Sum(*args: IntNumRef) -> IntNumRef: ...
def And(*args: BoolRef) -> BoolRef: ...
def Or(*args: BoolRef) -> BoolRef: ...
def Xor(a: BoolRef, b: BoolRef) -> BoolRef: ...
def Not(a: BoolRef) -> BoolRef: ...
def Implies(a: BoolRef, b: BoolRef, ctx: Context = ...) -> BoolRef: ...
def Distinct(*args: ExprRef) -> BoolRef: ...
def ForAll(
    vs: Const | Sequence[Const], body: ExprRef, qid: str = ""
) -> QuantifierRef: ...
def Exists(
    vs: Const | Sequence[Const], body: ExprRef, qid: str = ""
) -> QuantifierRef: ...
def Var(idx: int, s: SortRef) -> ExprRef: ...
def is_app_of(a: Any, op: int) -> bool: ...
def is_K(a: Any) -> TypeGuard[ArrayRef]: ...
def is_const_array(a: Any) -> TypeGuard[ArrayRef]: ...
def is_array(a: Any) -> TypeGuard[ArrayRef]: ...
def is_sort(a: Any) -> TypeGuard[SortRef]: ...
def is_ast(a: Any) -> TypeGuard[AstRef]: ...
def is_quantifier(a: Any) -> TypeGuard[QuantifierRef]: ...
def is_int(a: Any) -> TypeGuard[ArithRef]: ...
def is_app(a: Any) -> bool: ...
def is_eq(a: Any) -> TypeGuard[BoolRef]: ...
def is_distinct(a: Any) -> TypeGuard[BoolRef]: ...
def is_const(a: Any) -> TypeGuard[Const]: ...
def is_arith(a: Any) -> TypeGuard[ArithRef]: ...
def is_int_value(a: Any) -> TypeGuard[IntNumRef]: ...
def is_var(a: Any) -> bool: ...
def is_or(a: Any) -> TypeGuard[BoolRef]: ...
def is_and(a: Any) -> TypeGuard[BoolRef]: ...
def is_not(a: Any) -> TypeGuard[BoolRef]: ...
def is_implies(a: Any) -> TypeGuard[BoolRef]: ...
def is_lt(a: Any) -> bool: ...
def is_le(a: Any) -> bool: ...
def is_ge(a: Any) -> bool: ...
def is_gt(a: Any) -> bool: ...
def is_add(a: Any) -> bool: ...
def is_sub(a: Any) -> bool: ...
def is_mod(a: Any) -> bool: ...
def is_bool(a: Any) -> TypeGuard[BoolRef]: ...
def is_true(a: Any) -> TypeGuard[BoolRef]: ...
def is_false(a: Any) -> TypeGuard[BoolRef]: ...
def substitute_vars(t: AnyExprRef, *m: ExprRef) -> AnyExprRef: ...
def substitute(t: AnyExprRef, *m: tuple[ExprRef, ExprRef]) -> AnyExprRef: ...
def RoundTowardZero() -> ExprRef: ...
def set_param(*args: Any, **kwargs: Any) -> None: ...
def get_param(name: str) -> Any: ...
def reset_params() -> None: ...
def simplify(a: ExprRef, *arguments: Any, **keywords: Any) -> ExprRef: ...

sat: CheckSatResult = ...
unsat: CheckSatResult = ...
unknown: CheckSatResult = ...

Z3_OP_UNINTERPRETED: int = ...
Z3_OP_LT: int = ...
Z3_OP_LE: int = ...
Z3_OP_GE: int = ...
Z3_OP_GT: int = ...
Z3_OP_UMINUS: int = ...
Z3_UNINTERPRETED_SORT: int = ...
