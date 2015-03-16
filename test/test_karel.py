


def test__is_primitive_type():
  from genfrkl.karel import is_primitive_type

  for t in ['byte', 'short', 'integer', 'real', 'boolean']:
    assert True == is_primitive_type(t), "Fail for {}" .format(t)
    assert True == is_primitive_type(t.upper()), "Fail for {}" .format(t)

  #assert is_primitive_type('string')
  #assert is_primitive_type('STRING')

  # for now
  assert False == is_primitive_type('vector')
  assert False == is_primitive_type('position')
  assert False == is_primitive_type('xyzwpr')

  # non-karel types
  t_list = ['int8','uint8','int16','uint16','int32','uint32','int64','uint64','float32','float64']
  for t in t_list:
    assert False == is_primitive_type(t)


def test__primitive_zero_value():
  from genfrkl.karel import primitive_zero_value

  for t in ['byte', 'short', 'integer']:
    assert '0' == primitive_zero_value(t), "Fail for {}" .format(t)
    assert '0' == primitive_zero_value(t.upper()), "Fail for {}" .format(t)

  for t in ['real']:
    assert '0.0' == primitive_zero_value(t), "Fail for {}" .format(t)
    assert '0.0' == primitive_zero_value(t.upper()), "Fail for {}" .format(t)

  for t in ['boolean']:
    assert 'FALSE' == primitive_zero_value(t), "Fail for {}" .format(t)
    assert 'FALSE' == primitive_zero_value(t.upper()), "Fail for {}" .format(t)

  #for t in ['string']:
  #  assert "''" == primitive_zero_value(t), "Fail for {}" .format(t)
  #  assert "''" == primitive_zero_value(t.upper()), "Fail for {}" .format(t)


def test__is_too_long():
  from genfrkl.karel import is_too_long

  assert False == is_too_long('')
  assert False == is_too_long(' ')
  assert False == is_too_long(' '*12)
  assert False == is_too_long('short')

  assert True == is_too_long(' '*13)
  assert True == is_too_long('muchtoolongforkarel')


def test__is_legal_ident():
  from genfrkl.karel import is_legal_ident

  assert True == is_legal_ident('a')
  assert True == is_legal_ident('a1')
  assert True == is_legal_ident('a12345678901')

  # note: zero-length string and numeric first char is already checked
  #       by genmsg parser

  assert False == is_legal_ident('while')
  assert False == is_legal_ident('WHILE')
  assert False == is_legal_ident('program')
  assert False == is_legal_ident('time')

  assert True == is_legal_ident('something')
  assert True == is_legal_ident('_time')


def test__get_type_sz():
  from genfrkl.karel import get_type_sz

  for (t, sz,) in [('byte', 1), ('short', 2), ('integer', 4), ('real', 4), ('boolean', 4)]:
    assert sz == get_type_sz(t), "Fail for {}" .format(t)
    assert sz == get_type_sz(t.upper()), "Fail for {}" .format(t)

  try:
    fail_name = 'something_something'
    get_type_sz(fail_name)
    assert False, "should have failed type sz lookup for '%s'" % fail_name
  except KeyError:
    pass


def test__get_swap_function():
  from genfrkl.karel import get_swap_function

  expected_funcs = [('short', 'SWAP_SHORT'), ('integer', 'SWAP_INT'), ('real', 'SWAP_REAL')]

  for (t, fn) in expected_funcs:
    assert fn == get_swap_function(t), "Fail for {}" .format(t)
    assert fn == get_swap_function(t.upper()), "Fail for {}" .format(t)

  swap_fail_types = ['byte', 'char', 'nonsense', 'xyzwpr', '']
  for t in swap_fail_types:
    try:
      get_swap_function(t)
      assert False, "should have failed type swap func lookup for '%s'" % t
    except ValueError:
      pass

