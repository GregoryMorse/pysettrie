#!/usr/bin/env python3
# coding: utf8
"""
Unit tests for module PySetTrie (see settrie.py).

Author: Márton Miháltz 
https://sites.google.com/site/mmihaltz/
"""

import unittest
from settrie import SetTrie, SetTrieMap, SetTrieMultiMap

#unittest.main(settrie.TestSetTrie())

class TestSetTrie(unittest.TestCase):
  """
  UnitTest for SetTrie class
  """

  def setUp(self):
    self.t = SetTrie([{1, 3}, {1, 3, 5}, {1, 4}, {1, 2, 4}, {2, 4}, {2, 3, 5}])

  def test_print(self):
    expected = """None
  1
    2
      4#
    3#
      5#
    4#
  2
    3
      5#
    4#
"""
    from io import StringIO
    outp = StringIO()
    self.t.printtree(stream=outp)
    self.assertEqual(outp.getvalue(), expected)

  def test_iter(self):
    a = []
    for s in self.t:
      a.append(s)
    self.assertEqual(a, [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])

  def test_iter2(self):
    it = iter(self.t)
    for s in it:
      pass
    self.assertRaises(StopIteration, it.__next__)

  def test_iter3(self):
    t2 = SetTrie()
    it = iter(t2)
    self.assertRaises(StopIteration, it.__next__)

  def test_aslist(self):
    self.assertEqual(self.t.aslist(), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])
    
  def test_str(self):
    self.assertEqual(str(self.t), "[{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}]")

  def test_contains(self):
    self.assertTrue(self.t.contains( {1, 3} ))
    self.assertFalse(self.t.contains( {1} ))
    self.assertTrue(self.t.contains( {1, 3, 5} ))
    self.assertFalse(self.t.contains( {1, 3, 5, 7} ))

  def test_in(self):
    self.assertTrue({1, 3} in self.t)
    self.assertFalse({1} in self.t)
    self.assertTrue({1, 3, 5} in self.t)
    self.assertFalse({1, 3, 5, 7} in self.t)
    
  def test_hassuperset(self):
    self.assertTrue(self.t.hassuperset({3, 5}))
    self.assertFalse(self.t.hassuperset({6}))
    self.assertTrue(self.t.hassuperset({1, 2, 4}))
    self.assertFalse(self.t.hassuperset({2, 4, 5} ))
    self.assertFalse(SetTrie().hassuperset({}))
    
  def test_supersets(self):
    self.assertEqual(self.t.supersets({3, 5}), [{1, 3, 5}, {2, 3, 5}])
    self.assertEqual(self.t.supersets({1, 4}), [{1, 2, 4}, {1, 4}])
    self.assertEqual(self.t.supersets({1, 3, 5}),  [{1, 3, 5}])
    self.assertEqual(self.t.supersets({2}),  [{1, 2, 4}, {2, 3, 5}, {2, 4}])
    self.assertEqual(self.t.supersets({1}),  [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}])
    self.assertEqual(self.t.supersets({1, 2, 5}),  [])
    self.assertEqual(self.t.supersets({1, 2, 4, 5}),  [])
    self.assertEqual(self.t.supersets({6}),  [])

  def test_hassubset(self):
    self.assertTrue(self.t.hassubset({1, 2, 3}))
    self.assertTrue(self.t.hassubset({2, 3, 4, 5}))
    self.assertTrue(self.t.hassubset({1, 4}))
    self.assertTrue(self.t.hassubset({2, 3, 5}))
    self.assertFalse(self.t.hassubset({3, 4, 5}))
    self.assertFalse(self.t.hassubset({6, 7, 8, 9, 1000}))

  def test_subsets(self):
    self.assertEqual(self.t.subsets({1, 2, 4, 11}), [{1, 2, 4}, {1, 4}, {2, 4}])
    self.assertEqual(self.t.subsets({1, 2, 4}), [{1, 2, 4}, {1, 4}, {2, 4}])
    self.assertEqual(self.t.subsets({1, 2}), [])
    self.assertEqual(self.t.subsets({1, 2, 3, 4, 5}), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])
    self.assertEqual(self.t.subsets({0, 1, 3, 5}), [{1, 3}, {1, 3, 5}])
    self.assertEqual(self.t.subsets({1, 2, 5}), [])
    self.assertEqual(self.t.subsets({1, 4}), [{1, 4}]) # :)   
    self.assertEqual(self.t.subsets({1, 3, 5}), [{1, 3}, {1, 3, 5}])
    self.assertEqual(self.t.subsets({1, 3, 5, 111}), [{1, 3}, {1, 3, 5}])
    self.assertEqual(self.t.subsets({1, 4, 8}), [{1, 4}])
    self.assertEqual(self.t.subsets({2, 3, 4, 5}), [{2, 3, 5}, {2, 4}])
    self.assertEqual(self.t.subsets({2, 3, 5, 6}), [{2, 3, 5}])
  
  def test_add_remove(self):
    self.t.remove({1,3})
    self.assertEqual(self.t.aslist(), [{1, 2, 4}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])
    self.t.remove({1,3,5})
    self.assertEqual(self.t.aslist(), [{1, 2, 4}, {1, 4}, {2, 3, 5}, {2, 4}])
    self.t.remove({1,4})
    self.assertEqual(self.t.aslist(), [{1, 2, 4}, {2, 3, 5}, {2, 4}])
    self.t.remove({1,2,4})
    self.assertEqual(self.t.aslist(), [{2, 3, 5}, {2, 4}])
    self.t.remove({2,4})
    self.assertEqual(self.t.aslist(), [{2, 3, 5}])
    self.t.remove({2,3,5})
    self.assertEqual(self.t.aslist(), [])
    self.assertTrue(self.t.empty())
    self.t.add({1,3})
    self.assertEqual(self.t.aslist(), [{1, 3}])
    self.t.add({1,3,5})
    self.assertEqual(self.t.aslist(), [{1, 3}, {1, 3, 5}])
    self.t.add({1,4})
    self.assertEqual(self.t.aslist(), [{1, 3}, {1, 3, 5}, {1, 4}])
    self.t.add({1,2,4})
    self.assertEqual(self.t.aslist(), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}])
    self.t.add({2,4})
    self.assertEqual(self.t.aslist(), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 4}])
    self.t.add({2,3,5})
    self.assertEqual(self.t.aslist(), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])
  
  def test_validity(self):
    import numpy as np
    r = np.arange(30)
    t = SetTrie()
    count = 0
    for i in range(10000):
        np.random.shuffle(r)
        n = r[:np.random.randint(30)]
        if not n in t: count += 1
        t.add(n)
        t.add(n)
    self.assertEqual(count, len(list(t)))
    for i in range(100):
        np.random.shuffle(r)
        n = r[:np.random.randint(30)]
        ns, res = set(n), list()
        for x in t:
            if x.issubset(ns): res.append(x)
        self.assertEqual(t.hassubset(ns), not not res)
        self.assertEqual(list(t.itersubsets(ns)), res)
        res = list()
        for x in t:
            if x.issuperset(ns): res.append(x)
        self.assertEqual(t.hassuperset(ns), not not res)
        self.assertEqual(list(t.itersupersets(ns)), res)
        
  def test_performance(self):
    import numpy as np
    rnd = np.random.RandomState(0)
    r = np.arange(30)
    t = SetTrie()
    for i in range(10000):
        rnd.shuffle(r)
        n = r[:rnd.randint(30)]
        t.add(n)
        t.add(n)
    for i in range(10): list(t)
    for i in range(10000):
        rnd.shuffle(r)
        n = r[:rnd.randint(30)]
        list(t.itersubsets(n))
        t.hassubset(n)
        list(t.itersupersets(n))
        t.hassuperset(n)
        
class TestSetTrieRecursion(TestSetTrie):
  def setUp(self):
    self.t = SetTrie([{1, 3}, {1, 3, 5}, {1, 4}, {1, 2, 4}, {2, 4}, {2, 3, 5}], recursion=True)

class TestSetTrieItemStack(TestSetTrie):
  def setUp(self):
    self.t = SetTrie([{1, 3}, {1, 3, 5}, {1, 4}, {1, 2, 4}, {2, 4}, {2, 3, 5}], recursion=None)

class TestSetTrieMap(unittest.TestCase):
    """
    UnitTest for SetTrieMap class
    """

    def setUp(self):
        self.t = SetTrieMap([({1, 3}, 'A'), ({1, 3, 5}, 'B'), ({1, 4}, 'C'),
                             ({1, 2, 4}, 'D'), ({2, 4}, 'E'), ({2, 3, 5}, 'F')])
        # self.t.printtree()

    def test_print(self):
        expected = \
            """None
  1
    2
      4: 'D'
    3: 'A'
      5: 'B'
    4: 'C'
  2
    3
      5: 'F'
    4: 'E'
"""
        from io import StringIO
        outp = StringIO()
        self.t.printtree(stream=outp)
        self.assertEqual(outp.getvalue(), expected)

    def test_contains(self):
        self.assertTrue(self.t.contains({1, 3}))
        self.assertFalse(self.t.contains({1}))
        self.assertTrue(self.t.contains({1, 3, 5}))
        self.assertFalse(self.t.contains({1, 3, 5, 7}))

    def test_in(self):
        self.assertTrue({1, 3} in self.t)
        self.assertFalse({1} in self.t)
        self.assertTrue({1, 3, 5} in self.t)
        self.assertFalse({1, 3, 5, 7} in self.t)

    def test_get(self):
        self.assertEqual(self.t.get({1, 3}), 'A')
        self.assertEqual(self.t.get({1, 3, 5}), 'B')
        self.assertEqual(self.t.get({1, 4}), 'C')
        self.assertEqual(self.t.get({1, 2, 4}), 'D')
        self.assertEqual(self.t.get({2, 4}), 'E')
        self.assertEqual(self.t.get({2, 3, 5}), 'F')
        self.assertEqual(self.t.get({1, 2, 3}), None)
        self.assertEqual(self.t.get({100, 101, 102}, 0xDEADBEEF), 0xDEADBEEF)
        self.assertEqual(self.t.get({}), None)

    def test_assign(self):
        self.assertEqual(self.t.get({1, 3}), 'A')
        self.t.assign({1, 3}, 'AAA')
        self.assertEqual(self.t.get({1, 3}), 'AAA')
        self.assertEqual(self.t.get({100, 200}), None)
        self.t.assign({100, 200}, 'FOO')
        self.assertEqual(self.t.get({100, 200}), 'FOO')
        self.setUp()

    def test_hassuperset(self):
        self.assertTrue(self.t.hassuperset({3, 5}))
        self.assertFalse(self.t.hassuperset({6}))
        self.assertTrue(self.t.hassuperset({1, 2, 4}))
        self.assertFalse(self.t.hassuperset({2, 4, 5}))

    def test_supersets(self):
        self.assertEqual(self.t.supersets({3, 5}), [({1, 3, 5}, 'B'), ({2, 3, 5}, 'F')])
        self.assertEqual(self.t.supersets({1}), [({1, 2, 4}, 'D'), ({1, 3}, 'A'), ({1, 3, 5}, 'B'), ({1, 4}, 'C')])
        self.assertEqual(self.t.supersets({1, 2, 5}), [])
        self.assertEqual(self.t.supersetskeys({3, 5}), [{1, 3, 5}, {2, 3, 5}])
        self.assertEqual(self.t.supersetskeys({1}), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}])
        self.assertEqual(self.t.supersetskeys({1, 2, 5}), [])
        self.assertEqual(self.t.supersetsvalues({3, 5}), ['B', 'F'])
        self.assertEqual(self.t.supersetsvalues({1}), ['D', 'A', 'B', 'C'])
        self.assertEqual(self.t.supersetsvalues({1, 2, 5}), [])

    def test_hassubset(self):
        self.assertTrue(self.t.hassubset({1, 2, 3}))
        self.assertTrue(self.t.hassubset({2, 3, 4, 5}))
        self.assertTrue(self.t.hassubset({1, 4}))
        self.assertTrue(self.t.hassubset({2, 3, 5}))
        self.assertFalse(self.t.hassubset({3, 4, 5}))
        self.assertFalse(self.t.hassubset({6, 7, 8, 9, 1000}))

    def test_subsets(self):
        self.assertEqual(self.t.subsets({1, 2, 4, 11}), [({1, 2, 4}, 'D'), ({1, 4}, 'C'), ({2, 4}, 'E')])
        self.assertEqual(self.t.subsets({1, 2, 4}), [({1, 2, 4}, 'D'), ({1, 4}, 'C'), ({2, 4}, 'E')])
        self.assertEqual(self.t.subsets({1, 2}), [])
        self.assertEqual(self.t.subsets({1, 2, 3, 4, 5}), [({1, 2, 4}, 'D'), ({1, 3}, 'A'), ({1, 3, 5}, 'B'),
                                                           ({1, 4}, 'C'), ({2, 3, 5}, 'F'), ({2, 4}, 'E')])
        self.assertEqual(self.t.subsets({0, 1, 3, 5}), [({1, 3}, 'A'), ({1, 3, 5}, 'B')])
        self.assertEqual(self.t.subsets({1, 2, 5}), [])
        self.assertEqual(self.t.subsetskeys({1, 2, 4, 11}), [{1, 2, 4}, {1, 4}, {2, 4}])
        self.assertEqual(self.t.subsetskeys({1, 2, 4}), [{1, 2, 4}, {1, 4}, {2, 4}])
        self.assertEqual(self.t.subsetskeys({1, 2}), [])
        self.assertEqual(self.t.subsetskeys({1, 2, 3, 4, 5}), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5},
                                                                        {2, 4}])
        self.assertEqual(self.t.subsetskeys({0, 1, 3, 5}), [{1, 3}, {1, 3, 5}])
        self.assertEqual(self.t.subsetskeys({1, 2, 5}), [])
        self.assertEqual(self.t.subsetsvalues({1, 2, 4, 11}), ['D', 'C', 'E'])
        self.assertEqual(self.t.subsetsvalues({1, 2, 4}), ['D', 'C', 'E'])
        self.assertEqual(self.t.subsetsvalues({1, 2}), [])
        self.assertEqual(self.t.subsetsvalues({1, 2, 3, 4, 5}), ['D', 'A', 'B', 'C', 'F', 'E'])
        self.assertEqual(self.t.subsetsvalues({0, 1, 3, 5}), ['A', 'B'])
        self.assertEqual(self.t.subsetsvalues({1, 2, 5}), [])
        self.assertEqual(self.t.subsets({1, 4}), [({1, 4}, 'C')])
        self.assertEqual(self.t.subsets({1, 3, 5}), [({1, 3}, 'A'), ({1, 3, 5}, 'B')])
        self.assertEqual(self.t.subsets({1, 3, 5, 111}), [({1, 3}, 'A'), ({1, 3, 5}, 'B')])
        self.assertEqual(self.t.subsets({1, 4, 8}), [({1, 4}, 'C')])
        self.assertEqual(self.t.subsets({2, 3, 4, 5}), [({2, 3, 5}, 'F'), ({2, 4}, 'E')])
        self.assertEqual(self.t.subsets({2, 3, 5, 6}), [({2, 3, 5}, 'F')])

    def test_iters(self):
        self.assertEqual(self.t.aslist(), [({1, 2, 4}, 'D'), ({1, 3}, 'A'), ({1, 3, 5}, 'B'), ({1, 4}, 'C'),
                                           ({2, 3, 5}, 'F'), ({2, 4}, 'E')])
        self.assertEqual(list(self.t.keys()), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])
        self.assertEqual(list(self.t.values()), ['D', 'A', 'B', 'C', 'F', 'E'])
        self.assertEqual(list(self.t.__iter__()), list(self.t.keys()))

class TestSetTrieMultiMap(unittest.TestCase):
    """
    UnitTest for SetTrieMultiMap class
    """

    def setUp(self):
        self.t = SetTrieMultiMap([({1, 3}, 'A'), ({1, 3}, 'AA'), ({1, 3, 5}, 'B'), ({1, 4}, 'C'), ({1, 4}, 'CC'),
                                  ({1, 2, 4}, 'D'), ({1, 2, 4}, 'DD'), ({2, 4}, 'E'), ({2, 3, 5}, 'F'),
                                  ({2, 3, 5}, 'FF'), ({2, 3, 5}, 'FFF')])

    def test_aslist(self):
        self.assertEqual(self.t.aslist(), [({1, 2, 4}, 'D'), ({1, 2, 4}, 'DD'), ({1, 3}, 'A'), ({1, 3}, 'AA'),
                                           ({1, 3, 5}, 'B'), ({1, 4}, 'C'), ({1, 4}, 'CC'), ({2, 3, 5}, 'F'),
                                           ({2, 3, 5}, 'FF'), ({2, 3, 5}, 'FFF'), ({2, 4}, 'E')])

    def test_assign_returned_value(self):
        x = SetTrieMultiMap()
        self.assertEqual(x.assign({1, 3}, 'A'), 1)
        self.assertEqual(x.assign({1, 3}, 'AA'), 2)
        self.assertEqual(x.assign({1, 3}, 'A'), 3)
        self.assertEqual(x.assign({2, 4, 5}, 'Y'), 1)

    def test_count(self):
        self.assertEqual(self.t.count({1, 3}), 2)
        self.assertEqual(self.t.count({1, 3, 5}), 1)
        self.assertEqual(self.t.count({1, 3, 4}), 0)
        self.assertEqual(self.t.count({111, 222}), 0)
        self.assertEqual(self.t.count({2, 3, 5}), 3)

    def test_iterget(self):
        self.assertEqual(list(self.t.iterget({1, 3})), ['A', 'AA'])
        self.assertEqual(list(self.t.iterget({1, 3, 4})), [])

    def test_get(self):
        self.assertEqual(self.t.get({1, 3}), ['A', 'AA'])
        self.assertEqual(self.t.get({1, 2, 4}), ['D', 'DD'])
        self.assertEqual(self.t.get({1, 3, 5}), ['B'])
        self.assertEqual(self.t.get({2, 3, 5}), ['F', 'FF', 'FFF'])
        self.assertEqual(self.t.get({2, 4}), ['E'])
        self.assertEqual(self.t.get({1, 3, 4}), None)
        self.assertEqual(self.t.get({44}, []), [])

    def test_hassuperset(self):
        self.assertTrue(self.t.hassuperset({3, 5}))
        self.assertFalse(self.t.hassuperset({6}))
        self.assertTrue(self.t.hassuperset({1, 2, 4}))
        self.assertFalse(self.t.hassuperset({2, 4, 5}))

    def test_supersets(self):
        self.assertEqual(self.t.supersets({3, 5}), [({1, 3, 5}, 'B'), ({2, 3, 5}, 'F'), ({2, 3, 5}, 'FF'),
                                                    ({2, 3, 5}, 'FFF')])
        self.assertEqual(self.t.supersetsvalues({3, 5}), ['B', 'F', 'FF', 'FFF'])
        self.assertEqual(self.t.supersetskeys({3, 5}), [{1, 3, 5}, {2, 3, 5}])
        self.assertEqual(self.t.supersets({1}), [({1, 2, 4}, 'D'), ({1, 2, 4}, 'DD'), ({1, 3}, 'A'),
                                                 ({1, 3}, 'AA'), ({1, 3, 5}, 'B'), ({1, 4}, 'C'),
                                                 ({1, 4}, 'CC')])
        self.assertEqual(self.t.supersetskeys({1}), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}])
        self.assertEqual(self.t.supersetsvalues({1}), ['D', 'DD', 'A', 'AA', 'B', 'C', 'CC'])
        self.assertEqual(self.t.supersets({1, 2, 5}), [])
        self.assertEqual(self.t.supersetskeys({1, 2, 5}), [])
        self.assertEqual(self.t.supersetsvalues({1, 2, 5}), [])

    def test_hassubset(self):
        self.assertTrue(self.t.hassubset({1, 2, 3}))
        self.assertTrue(self.t.hassubset({2, 3, 4, 5}))
        self.assertTrue(self.t.hassubset({1, 4}))
        self.assertTrue(self.t.hassubset({2, 3, 5}))
        self.assertFalse(self.t.hassubset({3, 4, 5}))
        self.assertFalse(self.t.hassubset({6, 7, 8, 9, 1000}))

    def test_subsets(self):
        self.assertEqual(self.t.subsets({1, 2, 4, 11}), [({1, 2, 4}, 'D'), ({1, 2, 4}, 'DD'), ({1, 4}, 'C'),
                                                         ({1, 4}, 'CC'), ({2, 4}, 'E')])
        self.assertEqual(self.t.subsetskeys({1, 2, 4, 11}), [{1, 2, 4}, {1, 4}, {2, 4}])
        self.assertEqual(self.t.subsetsvalues({1, 2, 4, 11}), ['D', 'DD', 'C', 'CC', 'E'])
        self.assertEqual(self.t.subsets({1, 2, 4}), [({1, 2, 4}, 'D'), ({1, 2, 4}, 'DD'), ({1, 4}, 'C'), ({1, 4}, 'CC'),
                                                     ({2, 4}, 'E')])
        self.assertEqual(self.t.subsetskeys({1, 2, 4}), [{1, 2, 4}, {1, 4}, {2, 4}])
        self.assertEqual(self.t.subsetsvalues({1, 2, 4}), ['D', 'DD', 'C', 'CC', 'E'])
        self.assertEqual(self.t.subsets({1, 2}), [])
        self.assertEqual(self.t.subsetskeys({1, 2}), [])
        self.assertEqual(self.t.subsetsvalues({1, 2}), [])
        self.assertEqual(self.t.subsets({1, 2, 3, 4, 5}), [({1, 2, 4}, 'D'), ({1, 2, 4}, 'DD'), ({1, 3}, 'A'),
                                                           ({1, 3}, 'AA'), ({1, 3, 5}, 'B'), ({1, 4}, 'C'),
                                                           ({1, 4}, 'CC'), ({2, 3, 5}, 'F'), ({2, 3, 5}, 'FF'),
                                                           ({2, 3, 5}, 'FFF'), ({2, 4}, 'E')])
        self.assertEqual(self.t.subsets({1, 2, 3, 4, 5}), self.t.aslist())
        self.assertEqual(self.t.subsetskeys({1, 2, 3, 4, 5}), list(self.t.keys()))
        self.assertEqual(self.t.subsetskeys({1, 2, 3, 4, 5}), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5},
                                                                        {2, 4}])
        self.assertEqual(self.t.subsetsvalues({1, 2, 3, 4, 5}), ['D', 'DD', 'A', 'AA', 'B', 'C', 'CC', 'F',
                                                                          'FF', 'FFF', 'E'])
        self.assertEqual(self.t.subsetsvalues({1, 2, 3, 4, 5}), list(self.t.values()))
        self.assertEqual(self.t.subsets({0, 1, 3, 5}), [({1, 3}, 'A'), ({1, 3}, 'AA'), ({1, 3, 5}, 'B')])
        self.assertEqual(self.t.subsetskeys({0, 1, 3, 5}), [{1, 3}, {1, 3, 5}])
        self.assertEqual(self.t.subsetsvalues({0, 1, 3, 5}), ['A', 'AA', 'B'])
        self.assertEqual(self.t.subsets({1, 2, 5}), [])
        self.assertEqual(self.t.subsetskeys({1, 2, 5}), [])
        self.assertEqual(self.t.subsetsvalues({1, 2, 5}), [])
        self.assertEqual(self.t.subsets({1, 4}), [({1, 4}, 'C'), ({1, 4}, 'CC')])
        self.assertEqual(self.t.subsets({1, 3, 5}), [({1, 3}, 'A'), ({1, 3}, 'AA'), ({1, 3, 5}, 'B')])
        self.assertEqual(self.t.subsets({1, 3, 5, 111}), [({1, 3}, 'A'), ({1, 3}, 'AA'), ({1, 3, 5}, 'B')])
        self.assertEqual(self.t.subsets({1, 4, 8}), [({1, 4}, 'C'), ({1, 4}, 'CC')])
        self.assertEqual(self.t.subsets({2, 3, 4, 5}), [({2, 3, 5}, 'F'), ({2, 3, 5}, 'FF'), ({2, 3, 5}, 'FFF'),
                                                        ({2, 4}, 'E')])
        self.assertEqual(self.t.subsets({2, 3, 5, 6}), [({2, 3, 5}, 'F'), ({2, 3, 5}, 'FF'), ({2, 3, 5}, 'FFF')])

    # - - - - - - -

# If module is executed from command line, perform tests:
if __name__ == '__main__':
    unittest.main(verbosity=2)