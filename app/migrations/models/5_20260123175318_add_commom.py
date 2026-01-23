from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        COMMENT ON COLUMN "Card"."review_times" IS '卡片这次复习的次数';
        COMMENT ON COLUMN "Card"."title" IS '卡片标题';
        COMMENT ON COLUMN "Card"."created_at" IS '创建时间';
        COMMENT ON COLUMN "Card"."description" IS '卡片的详细内容';
        COMMENT ON COLUMN "Card"."review_at" IS '卡片这次复习时间';
        COMMENT ON COLUMN "Card"."summary" IS '卡片的概要信息(提示信息)';
        COMMENT ON COLUMN "Card"."updated_at" IS '更新时间';
        COMMENT ON COLUMN "Card"."user_id" IS '卡片所属用户ID';
        COMMENT ON COLUMN "Card"."is_star" IS '卡片是否收藏';
        COMMENT ON COLUMN "Card"."category_id" IS '卡片所属类别ID';
        COMMENT ON COLUMN "Category"."plan_id" IS '计划所属用户ID';
        COMMENT ON COLUMN "Category"."user_id" IS '分类所属用户ID';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        COMMENT ON COLUMN "Card"."review_times" IS NULL;
        COMMENT ON COLUMN "Card"."title" IS NULL;
        COMMENT ON COLUMN "Card"."created_at" IS NULL;
        COMMENT ON COLUMN "Card"."description" IS NULL;
        COMMENT ON COLUMN "Card"."review_at" IS NULL;
        COMMENT ON COLUMN "Card"."summary" IS NULL;
        COMMENT ON COLUMN "Card"."updated_at" IS NULL;
        COMMENT ON COLUMN "Card"."user_id" IS NULL;
        COMMENT ON COLUMN "Card"."is_star" IS NULL;
        COMMENT ON COLUMN "Card"."category_id" IS NULL;
        COMMENT ON COLUMN "Category"."plan_id" IS NULL;
        COMMENT ON COLUMN "Category"."user_id" IS NULL;"""


MODELS_STATE = (
    "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"
)
