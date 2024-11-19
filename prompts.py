#prompts


GENERATE_VIDEO_SUMMARY_PROMPT = ("These are frames from a video that I want to upload. Generate a summary that I can "
                                 "use compare video with image. Give me the each image summary text in List as "
                                 "your only output like ['Summary_1','Summary_2',...]")


GENERATE_IMAGE_SUMMARY_PROMPT = ("This is the image of a product that I want to upload. Generate a summary that I can "
                                 "use to compare image. Give me the summary text string as your only output.")


GENERATE_IMAGE_VIDEO_COMPARISION_PROMPT = ('Please analyze the main input image and all the frames to determine if '
                                           'the product is present in frames. If the main input image product is '
                                           'present in frames, provide "Yes"; if not, provide "No" . Output only one '
                                           'output in "Yes"/"No" .')

GENERATE_SEARCH_QUERY_PROMPT = ("""Generate a concise search query using the product's title and key details from its 
description. If the brand is mentioned, include it at the beginning. Exclude unrelated terms and keep the query short.
Product Title: {title}
Product Description: {description}
Return only the optimized search query.""")