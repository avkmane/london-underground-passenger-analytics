{% set hours = ['H05','H06','H07','H08','H09','H10','H11','H12','H13','H14','H15','H16','H17','H18','H19','H20','H21','H22','H23','H00','H01'] %}
{% for hour in hours %}
select Station as station, '{{ hour }}' as hour_code, {{ hour }}::bigint as exits from {{ ref('hourly_exits') }}
{% if not loop.last %} union all {% endif %}
{% endfor %}
