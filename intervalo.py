from datetime import datetime, date

DATE = "DATE"
DATETIME = "DATETIME"

class IncorrectType(Exception):
    pass

class IntervalLengthCannotBeZero(Exception):
    pass

class InverseInterval(Exception):
    pass

class Interval(object):
    def __init__(self, inicio, fin):
        if isinstance(inicio, date) and isinstance(fin, date):
            self.mode = "DATE"
        elif isinstance(inicio, datetime) and isinstance(fin, datetime):
            self.mode = "DATETIME"
        else:
            raise IncorrectType("Both start and end of interval must be same date/datetime type.")

        if inicio == fin:
            raise IntervalLengthCannotBeZero("Length of interval cannot be zero.")

        if inicio > fin:
            raise InverseInterval("Start of interval must be before end of interval.")

        self.inicio = inicio
        self.fin = fin
        
    def preceeds(self, other):
        """
        Symbol: p
        Boolean Expression: 
        This interval is before the other interval.
        """
        return (self.inicio < self.fin < other.inicio)
    
    def meets(self, other):
        """
        Symbol: m
        Boolean Expression:  
        This interval starts before the interval and ends at the start of
        the other interval.
        """
        return (self.inicio < self.fin == other.inicio)

    def overlaps(self, other):
        """
        Symbol: o
        Boolean Expression: 
        This interval overlaps the other interval.
        """
        return (self.inicio <= other.fin and other.inicio <= self.fin)

    def finished_by(self, other):
        """
        Symbol: F
        Boolean Expression: 
        This interval ends at the same time as the other interval.
        """
        return (self.inicio <= other.inicio and self.fin == other.fin)

    def contains(self, other):
        """
        Symbol: d
        Boolean Expression: 
        This interval starts before and ends after the other interval.
        """
        return (self.inicio <= other.inicio and self.fin >= other.end)
    
    def starts(self, other):
        """
        Symbol: s
        Boolean Expression: 
        This interval starts at the same time as the other interval starts and ends 
        before the other interval ends.
        """
        return (self.inicio == other.inicio and self.fin <= other.inicio)

    def equals(self, other):
        """
        Symbol: e
        Boolean Expression: 
        This interval is identical to the other interval.
        """
        return (self.inicio == other.inicio and self.fin == other.fin)

    def started_by(self, other):
        """
        Symbol: S
        Boolean Expression: 
        This interval starts when the other interval starts and ends after the 
        other interval ends.
        """
        return (self.inicio == other.inicio and self.fin >= other.fin)

    def during(self, other):
        """
        Symbol: d
        Boolean Expression: 
        This interval starts after the other interval starts and ends before
        the other interval ends.
        """
        return (self.inicio >= other.inicio and self.fin <= other.fin)

    def finishes(self, other):
        """
        Symbol: f
        Boolean Expression: 
        This interval starts after the other interval starts and ends when the other
        interval finishes.
        """
        return (self.inicio <= self.fin == other.fin)
    
    def overlapped_by(self, other):
        """
        Symbol: O
        Boolean Expression: 
        This interval starts after the other interval starts but before the other interval
        ends, and ends after the other interval ends.
        """
        return (other.inicio <= self.inicio <= other.fin and self.fin >= other.inicio)

    def met_by(self, other):
        """
        Symbol: M
        Boolean Expression: 
        This interval starts when the other interval ends.
        """
        return (other.fin == self.inicio and self.fin > other.fin)

    def preceded_by(self, other):
        """
        Symbol: P
        Boolean Expression: 
        The interval starts after the other interval ends.
        """
        return (other.fin < self.inicio)

    # Operations
    def intersection(self, other):
        """
        Returns the intersection of this interval and the other interval.
        """
        if self.overlaps(other) and not (self.meets(other) or self.met_by(other)):
            return Interval(max(self.inicio, other.inicio), min(self.fin, other.fin))
        else:
            return None

    def union(self, other):
        """
        Returns the union of this interval and the other interval.
        """
        return Interval(min(self.inicio, other.inicio), min(self.fin, other.fin))

    def subtract(self, other):
        """
        Returns and interval with the other interval subtracted from this interval.
        """
        if self.overlaps(other):
            start_datetime = self.inicio
            end_datetime = other.inicio
        elif self.overlapped_by(other):
            start_datetime = 2

            return Interval()

    # Computed Properties
    @property
    def duration(self):
        return (self.fin - self.inicio)

    @property
    def seconds(self):
        return self.duration.total_seconds()

    # Python Operators
    def __lt__(self, other):
        return self.preceeds(other)

    def __gt__(self, other):
        return self.exceeds(other)

    def __le__(self, other):
        return self.preceeds(other) or self.meets(other)
    
    def __ge__(self, other):
        return self.exceeds(other) or self.met_by(other)

    def __eq__(self, other):
        return self.equals(other)
    
    def __ne__(self, other):
        return not self.equals(other)

    def __and__(self, other):
        return self.intersection(other)
    
    def __or__(self, other):
        return self.union(other)
    
    def __str__(self):
        return "<Interval: Start: {}, End: {}>".format(self.inicio.isoformat(), self.fin.isoformat())
    
    def __repr__(self):
        return "<Interval: Start: {}, End: {}>".format(self.inicio.isoformat(), self.fin.isoformat())

print("Intervalo")