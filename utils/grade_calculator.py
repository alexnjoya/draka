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