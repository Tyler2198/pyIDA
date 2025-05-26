
# pyIDA

**pyIDA** is a Python package for Initial Data Analysis (IDA) in longitudinal studies, compliant with the STRATOS framework.

## Module: describe_participation()

- Inputs: long-format DataFrame with `subject_id`, `time_point`
- Outputs: Summary stats and heatmap of subject follow-up patterns

## Example
```python
from core.participation import describe_participation
summary = describe_participation(df, id_col='subject_id', time_col='visit_month')
```
