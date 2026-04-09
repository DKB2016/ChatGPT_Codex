from snippets.python.common.json_yaml_xml_patterns import parse_interfaces_xml


def test_parse_interfaces_xml_extracts_expected_fields() -> None:
    payload = """
    <interfaces>
      <interface>
        <name>GigabitEthernet1</name>
        <enabled>true</enabled>
        <description>Uplink</description>
      </interface>
    </interfaces>
    """

    parsed = parse_interfaces_xml(payload)

    assert len(parsed) == 1
    assert parsed[0]["name"] == "GigabitEthernet1"
    assert parsed[0]["admin_status"] == "true"
    assert parsed[0]["description"] == "Uplink"
