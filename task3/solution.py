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


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
