from app.filters.task_user_filter import filter_task_users
from app.tools.constants import AggregateMetric


def aggregate_tasks(
    metric,
    field=None,
    group_by=None,
    sort="desc",
    top_n=None,
    **filters
):

    tasks = filter_task_users(**filters)
    
    if tasks.empty:
        return []

    if isinstance(metric, AggregateMetric):
        metric = metric.value


    if metric == AggregateMetric.COUNT.value:

        if group_by:
            result = (
                tasks
                .groupby(group_by)
                .size()
                .reset_index(name="count")
            )

            result = result.sort_values(
                by="count",
                ascending=(sort == "asc")
            )

            if top_n:
                result = result.head(top_n)

            return result.to_dict(
                orient="records"
            )

        return len(tasks)


    elif metric == AggregateMetric.AVG.value:

        if not field:
            raise ValueError(
                "field is required for avg"
            )

        if group_by:
            result = (
                tasks
                .groupby(group_by)[field]
                .mean()
                .reset_index(name=f"avg_{field}")
            )

            result = result.sort_values(
                by=f"avg_{field}",
                ascending=(sort == "asc")
            )

            if top_n:
                result = result.head(top_n)

            return result.to_dict(
                orient="records"
            )

        return tasks[field].mean()


    elif metric == AggregateMetric.MIN.value:

        if not field:
            raise ValueError(
                "field is required for min"
            )

        if group_by:
            result = (
                tasks
                .groupby(group_by)[field]
                .min()
                .reset_index(name=f"min_{field}")
            )

            result = result.sort_values(
                by=f"min_{field}",
                ascending=(sort == "asc")
            )

            if top_n:
                result = result.head(top_n)

            return result.to_dict(
                orient="records"
            )

        return tasks[field].min()


    elif metric == AggregateMetric.MAX.value:

        if not field:
            raise ValueError(
                "field is required for max"
            )

        if group_by:
            result = (
                tasks
                .groupby(group_by)[field]
                .max()
                .reset_index(name=f"max_{field}")
            )

            result = result.sort_values(
                by=f"max_{field}",
                ascending=(sort == "asc")
            )

            if top_n:
                result = result.head(top_n)

            return result.to_dict(
                orient="records"
            )

        return tasks[field].max()


    elif metric == AggregateMetric.SUM.value:

        if not field:
            raise ValueError(
                "field is required for sum"
            )

        if group_by:
            result = (
                tasks
                .groupby(group_by)[field]
                .sum()
                .reset_index(name=f"sum_{field}")
            )

            result = result.sort_values(
                by=f"sum_{field}",
                ascending=(sort == "asc")
            )

            if top_n:
                result = result.head(top_n)

            return result.to_dict(
                orient="records"
            )

        return tasks[field].sum()

    raise ValueError(
        f"Unsupported metric: {metric}"
    )