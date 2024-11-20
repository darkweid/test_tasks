def merge_intervals(intervals: list) -> list:
    """Merge overlapping intervals into one continuous interval."""
    # Sorting the intervals is necessary, but we could skip this step if we knew that
    # the data were always sorted. However, the problem statement does not guarantee
    # that the intervals are pre-sorted.
    sorted_intervals = sorted(intervals)
    merged = []
    for start, end in sorted_intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def calculate_overlap(interval1: list, interval2: list) -> list:
    """Calculate the total overlap between two lists of intervals."""
    i, j = 0, 0
    total_overlap = 0
    while i < len(interval1) and j < len(interval2):
        start = max(interval1[i][0], interval2[j][0])
        end = min(interval1[i][1], interval2[j][1])
        if start < end:
            total_overlap += end - start
        if interval1[i][1] < interval2[j][1]:
            i += 1
        else:
            j += 1
    return total_overlap


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = [(intervals['lesson'][0], intervals['lesson'][1])]
    pupil_intervals = list(zip(intervals['pupil'][::2], intervals['pupil'][1::2]))
    tutor_intervals = list(zip(intervals['tutor'][::2], intervals['tutor'][1::2]))

    # Merge intervals for pupil and tutor
    merged_pupil = merge_intervals(pupil_intervals)
    merged_tutor = merge_intervals(tutor_intervals)

    # Calculate the overlap of merged tutor intervals with the lesson-pupil overlap
    combined_intervals = [(max(lesson[0][0], p[0]), min(lesson[0][1], p[1])) for p in merged_pupil]
    merged_combined_intervals = merge_intervals(combined_intervals)
    total_overlap = calculate_overlap(merged_combined_intervals, merged_tutor)

    return total_overlap
