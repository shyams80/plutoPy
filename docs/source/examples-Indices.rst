Using Indices
==============

..  code-block:: python

	"""This example illustrates how to get a list of all the latest NSE Indices"""
	
	from sqlalchemy import func
	from model import RoutingSession, Indices

	#a list of all current NSE indices
	end_dt = RoutingSession.session.query(func.max(Indices.NseTimeSeries.TIME_STAMP)).scalar()

	results = RoutingSession.session.query(Indices.NseTimeSeries.NAME).\
				filter(Indices.NseTimeSeries.TIME_STAMP == end_dt).all()

	print(f"fetched: {len(results)}")
	for instance in results:
		print(instance.NAME)
