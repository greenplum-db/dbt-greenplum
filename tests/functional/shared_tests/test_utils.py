import pytest

from dbt.tests.adapter.utils.test_any_value import BaseAnyValue
from dbt.tests.adapter.utils.test_array_append import BaseArrayAppend
from dbt.tests.adapter.utils.test_array_concat import BaseArrayConcat
from dbt.tests.adapter.utils.test_array_construct import BaseArrayConstruct
from dbt.tests.adapter.utils.test_bool_or import BaseBoolOr
from dbt.tests.adapter.utils.test_cast_bool_to_text import BaseCastBoolToText
from dbt.tests.adapter.utils.test_concat import BaseConcat
from dbt.tests.adapter.utils.test_current_timestamp import BaseCurrentTimestampAware
from dbt.tests.adapter.utils.test_dateadd import BaseDateAdd
from dbt.tests.adapter.utils.test_datediff import BaseDateDiff
from dbt.tests.adapter.utils.test_date_spine import BaseDateSpine
from dbt.tests.adapter.utils.test_date_trunc import BaseDateTrunc
from dbt.tests.adapter.utils.test_equals import BaseEquals
from dbt.tests.adapter.utils.test_escape_single_quotes import (
    BaseEscapeSingleQuotesQuote,
    BaseEscapeSingleQuotesBackslash,
)
from dbt.tests.adapter.utils.test_except import BaseExcept
from dbt.tests.adapter.utils.test_generate_series import BaseGenerateSeries
from dbt.tests.adapter.utils.test_get_intervals_between import BaseGetIntervalsBetween
from dbt.tests.adapter.utils.test_get_powers_of_two import BaseGetPowersOfTwo
from dbt.tests.adapter.utils.test_hash import BaseHash
from dbt.tests.adapter.utils.test_intersect import BaseIntersect
from dbt.tests.adapter.utils.test_last_day import BaseLastDay
from dbt.tests.adapter.utils.test_length import BaseLength
from dbt.tests.adapter.utils.test_listagg import BaseListagg
from dbt.tests.adapter.utils.test_null_compare import BaseNullCompare, BaseMixedNullCompare
from dbt.tests.adapter.utils.test_position import BasePosition
from dbt.tests.adapter.utils.test_replace import BaseReplace
from dbt.tests.adapter.utils.test_right import BaseRight
from dbt.tests.adapter.utils.test_safe_cast import BaseSafeCast
from dbt.tests.adapter.utils.test_split_part import BaseSplitPart
from dbt.tests.adapter.utils.test_string_literal import BaseStringLiteral
from dbt.tests.adapter.utils.test_timestamps import BaseCurrentTimestamps
from dbt.tests.adapter.utils.test_validate_sql import BaseValidateSqlMethod


class TestAnyValue(BaseAnyValue):
    pass


class TestArrayAppend(BaseArrayAppend):
    pass


class TestArrayConcat(BaseArrayConcat):
    pass


class TestArrayConstruct(BaseArrayConstruct):
    pass


class TestBoolOr(BaseBoolOr):
    pass


class TestCastBoolToText(BaseCastBoolToText):
    pass


class TestConcat(BaseConcat):
    pass


class TestCurrentTimestamp(BaseCurrentTimestampAware):
    pass

# Greenplum-Specific: using valid syntax for greenplum
# Theis model definition is taken from dbt.tests.adapter.utils fixture_date_spine.py.
# And we change them so that the syntax is valid for greenplum.
models__test_greenplum_date_spine_sql = """
with generated_dates as (
    {{ date_spine("day", "'2023-09-01'::date", "'2023-09-10'::date") }}
), expected_dates as (
    select '2023-09-01'::date as expected
    union all
    select '2023-09-02'::date as expected
    union all
    select '2023-09-03'::date as expected
    union all
    select '2023-09-04'::date as expected
    union all
    select '2023-09-05'::date as expected
    union all
    select '2023-09-06'::date as expected
    union all
    select '2023-09-07'::date as expected
    union all
    select '2023-09-08'::date as expected
    union all
    select '2023-09-09'::date as expected

), joined as (
    select
        generated_dates.date_day,
        expected_dates.expected
    from generated_dates
    left join expected_dates on generated_dates.date_day = expected_dates.expected
)

SELECT * from joined
"""

models__test_greenplum_date_spine_yml = """
version: 2
models:
  - name: test_greenplum_date_spine
    data_tests:
      - assert_equal:
          actual: date_day
          expected: expected
"""

class TestDateSpine(BaseDateSpine):
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "test_greenplum_date_spine.yml": models__test_greenplum_date_spine_yml,
            "test_greenplum_date_spine.sql": self.interpolate_macro_namespace(
                models__test_greenplum_date_spine_sql, "greenplum_date_spine"
            ),
        }    


class TestDateTrunc(BaseDateTrunc):
    pass


class TestDateAdd(BaseDateAdd):
    pass


class TestDateDiff(BaseDateDiff):
    pass


class TestEquals(BaseEquals):
    pass


class TestEscapeSingleQuotesQuote(BaseEscapeSingleQuotesQuote):
    pass


@pytest.mark.skip("Not implemented in `dbt-postgres<1.8`, fails in `dbt-postgres>=1.8`")
class TestEscapeSingleQuotesBackslash(BaseEscapeSingleQuotesBackslash):
    pass


class TestExcept(BaseExcept):
    pass


class TestGenerateSeries(BaseGenerateSeries):
    pass


class TestGetIntervalsBetween(BaseGetIntervalsBetween):
    pass


class TestGetPowersOfTwo(BaseGetPowersOfTwo):
    pass


class TestHash(BaseHash):
    pass


class TestIntersect(BaseIntersect):
    pass


class TestLastDay(BaseLastDay):
    pass


class TestLength(BaseLength):
    pass


class TestListagg(BaseListagg):
    pass


class TestMixedNullCompare(BaseMixedNullCompare):
    pass


class TestNullCompare(BaseNullCompare):
    pass


class TestPosition(BasePosition):
    pass


class TestReplace(BaseReplace):
    pass


class TestRight(BaseRight):
    pass


class TestSafeCast(BaseSafeCast):
    pass


class TestSplitPart(BaseSplitPart):
    pass


class TestStringLiteral(BaseStringLiteral):
    pass


class TestCurrentTimestamps(BaseCurrentTimestamps):
    pass


class TestValidateSqlMethod(BaseValidateSqlMethod):
    pass
