from app.filters.task_filters import filter_tasks
from app.filters.user_filters import filter_users
from app.filters.task_user_filter import filter_task_users

from app.tools.constants import (
    AggregateMetric,
    DataSource,
    SortOrder,
)


FILTERS = {
    DataSource.TASKS: filter_tasks,
    DataSource.USERS: filter_users,
    DataSource.TASK_USERS: filter_task_users,
}


def aggregate(
    source=DataSource.TASK_USERS,
    metric=AggregateMetric.COUNT,
    field=None,
    group_by=None,
    sort=SortOrder.DESC,
    top_n=None,
    **filters
):

    if isinstance(source, str):
        source = DataSource(source)

    if isinstance(metric, str):
        metric = AggregateMetric(metric)

    if isinstance(sort, str):
        sort = SortOrder(sort)

    if source not in FILTERS:
        raise ValueError(
            f"Unsupported source: {source}"
        )

    data = FILTERS[source](
        **filters
    )

    if data.empty:
        return []

    ascending = (
        sort == SortOrder.ASC
    )

    if metric == AggregateMetric.COUNT:

        if group_by:

            result = (
                data
                .groupby(group_by)
                .size()
                .reset_index(
                    name="count"
                )
            )

            result = result.sort_values(
                by="count",
                ascending=ascending,
            )

            if top_n:
                result = result.head(
                    top_n
                )

            return result.to_dict(
                orient="records"
            )

        return len(data)

    if metric == AggregateMetric.AVG:

        if not field:
            raise ValueError(
                "field is required for avg"
            )

        if group_by:

            result = (
                data
                .groupby(group_by)[field]
                .mean()
                .reset_index(
                    name=f"avg_{field}"
                )
            )

            result = result.sort_values(
                by=f"avg_{field}",
                ascending=ascending,
            )

            if top_n:
                result = result.head(
                    top_n
                )

            return result.to_dict(
                orient="records"
            )

        return data[field].mean()

    if metric == AggregateMetric.MIN:

        if not field:
            raise ValueError(
                "field is required for min"
            )

        if group_by:

            result = (
                data
                .groupby(group_by)[field]
                .min()
                .reset_index(
                    name=f"min_{field}"
                )
            )

            result = result.sort_values(
                by=f"min_{field}",
                ascending=ascending,
            )

            if top_n:
                result = result.head(
                    top_n
                )

            return result.to_dict(
                orient="records"
            )

        return data[field].min()

    if metric == AggregateMetric.MAX:

        if not field:
            raise ValueError(
                "field is required for max"
            )

        if group_by:

            result = (
                data
                .groupby(group_by)[field]
                .max()
                .reset_index(
                    name=f"max_{field}"
                )
            )

            result = result.sort_values(
                by=f"max_{field}",
                ascending=ascending,
            )

            if top_n:
                result = result.head(
                    top_n
                )

            return result.to_dict(
                orient="records"
            )

        return data[field].max()

    if metric == AggregateMetric.SUM:

        if not field:
            raise ValueError(
                "field is required for sum"
            )

        if group_by:

            result = (
                data
                .groupby(group_by)[field]
                .sum()
                .reset_index(
                    name=f"sum_{field}"
                )
            )

            result = result.sort_values(
                by=f"sum_{field}",
                ascending=ascending,
            )

            if top_n:
                result = result.head(
                    top_n
                )

            return result.to_dict(
                orient="records"
            )

        return data[field].sum()

    raise ValueError(
        f"Unsupported metric: {metric}"
    )