from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel
from typing import List

class ReportArgsSchema(BaseModel):
    report_name: str
    html: str

def write_report(report_name, html):
    with open(report_name, "w") as f:
        f.write(html)

write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="Use this to write an HTML report to a file",
    func=write_report,
    args_schema=ReportArgsSchema
)
