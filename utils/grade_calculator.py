def calculate_grade(score):
    """
    Calculate letter grade based on numerical score
    
    Args:
        score (int): Numerical score (0-100)
    
    Returns:
        str: Letter grade (A, B, C, D, F)
    """
    if score >= 80:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 60:
        return 'C'
    elif score >= 50:
        return 'D'
    else:
        return 'F'

def calculate_gpa_points(score):
    """
    Calculate GPA points based on numerical score
    
    Args:
        score (int): Numerical score (0-100)
    
    Returns:
        float: GPA points (4.0 scale)
    """
    if score >= 80:
        return 4.0
    elif score >= 70:
        return 3.0
    elif score >= 60:
        return 2.0
    elif score >= 50:
        return 1.0
    else:
        return 0.0

def get_grade_description(grade):
    """
    Get description for a letter grade
    
    Args:
        grade (str): Letter grade
    
    Returns:
        str: Grade description
    """
    descriptions = {
        'A': 'Excellent (80-100)',
        'B': 'Good (70-79)',
        'C': 'Average (60-69)',
        'D': 'Below Average (50-59)',
        'F': 'Fail (0-49)'
    }
    return descriptions.get(grade, 'Unknown Grade')

def validate_score(score):
    """
    Validate that score is within acceptable range
    
    Args:
        score (int): Score to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        score = int(score)
        return 0 <= score <= 100
    except (ValueError, TypeError):
        return False

def calculate_cumulative_gpa(records):
    """
    Calculate cumulative GPA from a list of academic records
    
    Args:
        records (list): List of academic records with 'gpa_points' and 'credits'
    
    Returns:
        float: Cumulative GPA
    """
    if not records:
        return 0.0
    
    total_points = 0
    total_credits = 0
    
    for record in records:
        if record.get('gpa_points') is not None and record.get('credits') is not None:
            total_points += record['gpa_points'] * record['credits']
            total_credits += record['credits']
    
    return round(total_points / total_credits, 2) if total_credits > 0 else 0.0