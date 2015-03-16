
def test__group_fields():
    from genfrkl import group_fields
    from genmsg.msg_loader import load_msg_from_string, MsgContext

    context = MsgContext.create_default()
    msg_txt = """
      Header header
      float32 x
      float64 y
      int32[5] arr_a
      uint16 z
      Float32 xx
      byte a
      Byte[3] arr_b
    """
    msgspec = load_msg_from_string(context, msg_txt, 'my_pkg/FieldGroupTest')
    groups = group_fields(msgspec)

    assert len(groups) == 7, "Expected 7 groups"
    assert len(groups[0]) == 1, "First group should have only one element"

    assert True == groups[6][0].is_array, "Last group should have single element, which is an array"

    assert len(groups[0]) == 1
    assert len(groups[1]) == 2
    assert len(groups[2]) == 1
    assert len(groups[3]) == 1
    assert len(groups[4]) == 1
    assert len(groups[5]) == 1
    assert len(groups[6]) == 1


def test__group_fields2():
    from genfrkl import group_fields
    from genmsg.msg_loader import load_msg_from_string, MsgContext

    context = MsgContext.create_default()
    msg_txt = """
      float32 x
    """
    msgspec = load_msg_from_string(context, msg_txt, 'my_pkg/FieldGroupTest')
    groups = group_fields(msgspec)

    assert len(groups) == 1, "Expected 1 groups"
    assert len(groups[0]) == 1, "First group should have only one element"


def test__group_fields3():
    from genfrkl import group_fields
    from genmsg.msg_loader import load_msg_from_string, MsgContext

    context = MsgContext.create_default()
    msg_txt = """
      Float32 x
      Float32[4] xx
      float32 z
      float32 zz
    """
    msgspec = load_msg_from_string(context, msg_txt, 'my_pkg/FieldGroupTest')
    groups = group_fields(msgspec)

    assert len(groups) == 3, "Expected 2 groups"
    assert len(groups[0]) == 1, "First group should have only one element"
    assert len(groups[1]) == 1, "Second group should have only one element"
    assert len(groups[2]) == 2, "Third group should have two elements"


def test__group_fields4():
    from genfrkl import group_fields
    from genmsg.msg_loader import load_msg_from_string, MsgContext

    context = MsgContext.create_default()
    msg_txt = """
    """
    msgspec = load_msg_from_string(context, msg_txt, 'my_pkg/FieldGroupTest')
    groups = group_fields(msgspec)

    assert len(groups) == 0, "Expected 0 groups"


def test__group_fields5():
    from genfrkl import group_fields
    from genmsg.msg_loader import load_msg_from_string, MsgContext

    context = MsgContext.create_default()
    msg_txt = """
      uint8 a
      uint16 b
      uint32 c
      uint32[3] d
      Int64 e
    """
    msgspec = load_msg_from_string(context, msg_txt, 'my_pkg/FieldGroupTest')
    groups = group_fields(msgspec)

    assert len(groups) == 3, "Expected 3 groups"


def test__group_fields5():
    from genfrkl import group_fields
    from genmsg.msg_loader import load_msg_from_string, MsgContext

    context = MsgContext.create_default()
    msg_txt = """
      uint32[4] a
      uint16[5] b
    """
    msgspec = load_msg_from_string(context, msg_txt, 'my_pkg/FieldGroupTest')
    groups = group_fields(msgspec)

    assert len(groups) == 2, "Expected 2 groups"
    assert len(groups[0]) == 1, "First group should have only one element"
    assert len(groups[1]) == 1, "Second group should have only one element"
