# pysettrie

[![CI](https://github.com/GregoryMorse/pysettrie/actions/workflows/ci.yml/badge.svg)](https://github.com/GregoryMorse/pysettrie/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/pysettrie.svg)](https://pypi.org/project/pysettrie/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysettrie)](https://pypi.org/project/pysettrie/)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

**pysettrie** is a high-performance [Cython](https://cython.org/) Python 3 library for efficient storage and querying of collections of sets using the [set-trie](http://osebje.famnit.upr.si/~savnik/papers/cdares13.pdf) data structure. It supports fast superset and subset search over large collections — far faster than naive iteration.

- **GitHub:** https://github.com/GregoryMorse/pysettrie
- **PyPI:** https://pypi.org/project/pysettrie/
- **Maintainer:** Gregory Morse &lt;gregory.morse@live.com&gt;

---

## Features

- Fast superset/subset queries over a stored collection of sets
- Three container types covering set-only, key→value, and key→multiple-values use cases
- Core algorithms implemented in Cython with C++ internals for maximum performance
- Pure Python fallback interface; drop-in for dict-of-sets workflows
- Fully unit-tested

---

## Installation

```bash
pip install pysettrie
```

> **Note:** A C++ compiler is required to build from source (the PyPI wheel is pre-built for common platforms). On Ubuntu you may need `sudo apt-get install build-essential` if building from source.

---

## Containers

| Class | Description |
|---|---|
| `SetTrie` | Set-trie container for a collection of sets. Supports fast superset/subset queries. |
| `SetTrieMap` | Mapping container with sets as keys. Like `SetTrie` but associates a single value with each key set. |
| `SetTrieMultiMap` | Like `SetTrieMap` but allows multiple values per key set. |

---

## Quick Start

```python
from settrie import SetTrie, SetTrieMap, SetTrieMultiMap

# --- SetTrie ---
t = SetTrie([{1, 3}, {1, 3, 5}, {1, 4}, {1, 2, 4}, {2, 4}, {2, 3, 5}])

t.contains({1, 3})          # True
t.hassuperset({3, 5})       # True  — is there any stored set that is a superset of {3,5}?
t.supersets({3, 5})         # [{1, 3, 5}, {2, 3, 5}]
t.hassubset({1, 2, 3})      # True  — is there any stored set that is a subset of {1,2,3}?
t.subsets({1, 2, 4})        # [{1, 2, 4}, {1, 4}, {2, 4}]

t.add({6, 7})
t.remove({1, 4})

# --- SetTrieMap ---
m = SetTrieMap()
m.assign({1, 2}, 'a')
m.assign({1, 2, 3}, 'b')
m.assign({3, 4}, 'c')

m.get({1, 2})               # 'a'
m.supersets({1})            # [({1, 2}, 'a'), ({1, 2, 3}, 'b')]
m.subsets({1, 2, 3, 4})     # [({1, 2}, 'a'), ({1, 2, 3}, 'b'), ({3, 4}, 'c')]

# --- SetTrieMultiMap ---
mm = SetTrieMultiMap()
mm.assign({1, 2}, 'x')
mm.assign({1, 2}, 'y')      # second value for same key
mm.get({1, 2})              # ['x', 'y']
```

---

## Background

pysettrie implements the set-trie data structure described in:

> I. Savnik: *Index data structure for fast subset and superset queries.* CD-ARES, IFIP LNCS, 2013.  
> http://osebje.famnit.upr.si/~savnik/papers/cdares13.pdf

**Notes on the paper:**
- Algorithm 1 does not mention sorting children during insert (line 5 should do a sorted insert).
- Algorithm 4 is incorrect and will always return false; line 7 should read: *"for (each child of node labeled l: word.currentElement ≤ l) & (while not found) do"*
- The descriptions of `getAllSubSets` and `getAllSuperSets` are wrong and would not produce all sub/supersets.

**See also:**
- https://stackoverflow.com/questions/9353100/quickly-checking-if-set-is-superset-of-stored-sets
- https://stackoverflow.com/questions/1263524/superset-search

---

## Performance

The original pure-Python `settrie` module was rewritten entirely in Cython with C++ (`std::set`, `std::vector`, `std::stack`) underlying data structures. This yields significantly faster insertion, lookup, and query performance compared to the pure-Python implementation, especially for large collections.

---

## Running Tests

```bash
python -m pytest tests/
```

---

## Changelog

### Version 1.0.3
- Switch to GitHub Actions CI; update README and badges.

### Version 1.0.2
- Continuous integration, remove unnecessary files, improve build requirements.

### Version 1.0.0
- Complete Cython rewrite for improved performance; bug fixes.

### Version 0.1.3 (original pure-Python release by Márton Miháltz)
- `SetTrieMultiMap.assign()` returns number of values associated to key after assignment.

---

## Authors

- **Gregory Morse** &lt;gregory.morse@live.com&gt; — Cython rewrite, current maintainer  
  GitHub: [GregoryMorse](https://github.com/GregoryMorse)
- **Márton Miháltz** — Original pure-Python implementation  
  https://sites.google.com/site/mmihaltz/

---

## License

Licensed under the [GNU Lesser General Public License v3 (LGPLv3)](https://www.gnu.org/licenses/lgpl-3.0.html).

