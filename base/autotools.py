from hashdist import build_stage

@build_stage()
def configure(ctx, stage):
    lines = ['./configure --prefix="${ARTIFACT}"']
    return lines
