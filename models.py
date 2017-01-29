"""Models."""


class pyChart(object):
    def __init__(self, chartType, renderTo, title, subtitle=None, xLab=None, yLab=None, series=None, credits=None):
        self.chartType = chartType

        if series:
            self.series = series
        else:
            self.series = []

        self.chart = {
            'chart': {
                'type': chartType,
                'renderTo': renderTo
            },
            'title': {
                'text': ''
            },
            'series': self.series
        }

        if chartType in ['column', 'bar', 'line', 'spline']:
            if yLab:
                self.chart['yAxis'] = {'title': {'text': yLab}}
            else:
                self.chart['yAxis'] = {'title': {'enabled': 0}}
            self.chart['xAxis'] = {'categories': xLab}
        elif chartType in ['pie']:
            self.chart['series'] = [{'name': xLab, 'colorByPoint': 1, 'data': []}]
        elif chartType in ['scatter', 'bubble']:
            self.chart['yAxis'] = {'title': {'text': yLab}}
            self.chart['xAxis'] = {'title': {'text': xLab}}
        else:
            pass

        if credits:
            self.chart['credits'] = {'text': credits[0], 'href': credits[1]}
        else:
            self.chart['credits'] = {'enabled': 0}

        if subtitle:
            self.chart['subtitle'] = {'text': subtitle}

    def addToSeries(self, name, data):  # TODO: create a showInLegend function to customize legend
        if self.chartType in ['column', 'bar', 'line', 'spline']:
            self.chart['series'].append({'name': name, 'data': data, 'showInLegend': 0})
        elif self.chartType in ['pie']:
            self.chart['series'][0]['data'].append({'name': name, 'data': data, 'showInLegend': 0})
        elif self.chartType in ['scatter', 'bubble']:
            self.chartType['series'][0]['data'].append({'name': name, 'data': data, 'showInLegend': 0})
        else:
            pass

    def formatPoint(self, format):
        self.chart['tooltip'] = {'pointFormat': format}

    def yAxisMax(self, value):
        self.chart['yAxis']['max'] = value

    def generate(self):
        return self.chart
