{% macro storage_parameters(appendoptimized, blocksize, orientation, compresstype, compresslevel) %}
    {% set storage_parameters %}
        {% if appendoptimized %}
            with (
                appendoptimized={{ appendoptimized }}
                , blocksize={{ blocksize }}
                , compresstype={{ compresstype }}
                , compresslevel={{ compresslevel }}
                , orientation={{ orientation }}
            )
        {% endif %}
    {% endset %}

    {{ return(storage_parameters) }}
{% endmacro %}